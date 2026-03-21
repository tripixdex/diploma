using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using System.Windows.Forms;
using YaClass;
namespace Warehouse
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            timer.Tick += new EventHandler(label1_Click); // обновление лейблов интерфейса по времени
            timer.Tick += new EventHandler(label11_Click);
            timer.Tick += new EventHandler(label16_Click);
            timer.Tick += new EventHandler(label17_Click);
            timer.Interval = 500;
            timer.Start();

        }
        System.Windows.Forms.Timer timer = new System.Windows.Forms.Timer();
        public bool working = false; // false - не перемещается, true - перемещается
        public bool autonomus = false;
        public string recieved_data = "";
        private const string DeviceID = "are18v6krffaq7o1mldk"; // my cloud are7vm1sa8h0pr5duead
                                                                // are18v6krffaq7o1mldk semen cloud
        string[] commands;
        // used for login-password authentication
        private const string RegistryID = "aresgcakub7pk92mbhej"; // my cloud areese9ohba65k0nrln9
                                                                  // aresgcakub7pk92mbhej semen cloud
        private const string RegistryPassword = "Adminsklad2020";
        private const string DevicePassword = "Adminsklad2020";
        private YaClient devClient = new YaClient();
        public bool isconnected = false;
        public bool auto = false;
        public int row_counter = 1;
        public int column_counter = 1;
        public String test_topic = "$devices/are18v6krffaq7o1mldk/events/test";
        string topic = YaClient.TopicName(DeviceID, EntityType.Device, TopicType.Commands);
        public volatile Queue<String> q_from_cloud = new Queue<string>();
        public volatile Queue<String> q_from_reader = new Queue<string>();
        public volatile Queue<String> q_from_conveyor = new Queue<string>();
        private void virtual_plc_run() {
            axMintController1.SetVirtualControllerLink();
            axMintController1.set_TriggerMode(0, 0);
            axMintController1.set_TriggerMode(1, 0);
            axMintController1.set_TriggerMode(2, 0); }
        private void plc_run() {
            axMintController1.SetUSBControllerLink(2); // создаю подключение с ПЛК по USB
            axMintController1.set_Comms(36, 1); // записываю в регистры памяти ПЛК, чтобы разблокировать движение по осям (системное ПО ПЛК блочит)
            axMintController1.set_Comms(1, 36);
            axMintController1.set_Comms(8, 1);
            axMintController1.set_Comms(14, 40000);
            axMintController1.set_Comms(39, 200);
            if (!axMintController1.MintExecuting) { axMintController1.DoMintRun(); } } // если прошивка не запущена, запустить
        private void Form1_Load(object sender, EventArgs e) { virtual_plc_run(); } // запуск системого ПО ПЛК

        private void axMintController1_SerialReceiveEvent(object sender, EventArgs e) { }

        private void button3_Click(object sender, EventArgs e) { axMintController1.set_MoveR(0, 1000); }

        private void button4_Click(object sender, EventArgs e) { axMintController1.set_MoveR(0, -1000); }

        private void button5_Click(object sender, EventArgs e) { axMintController1.set_MoveR(1, 1000); }

        private void button6_Click(object sender, EventArgs e) { axMintController1.set_MoveR(1, -1000); }

        private void button7_Click(object sender, EventArgs e) { axMintController1.set_MoveR(2, 1000); }

        private void button8_Click(object sender, EventArgs e) { axMintController1.set_MoveR(2, -1000); }

        async public void button9_Click(object sender, EventArgs e) { await Task.Run(() => GoHome()); }

        private void label1_Click(object sender, EventArgs e) {
            string s = "";
            s = axMintController1.get_Pos(0).ToString() + "\n" +
                axMintController1.get_Pos(1).ToString() +
                "\n" + axMintController1.get_Pos(2).ToString();
            label1.Text = s; }
        private void button10_Click(object sender, EventArgs e) {
            if (axMintController1.get_DriveEnable(0) || axMintController1.get_DriveEnable(1)
                || axMintController1.get_DriveEnable(2) == false) {
                axMintController1.set_DriveEnable(0, true);
                axMintController1.set_DriveEnable(1, true);
                axMintController1.set_DriveEnable(2, true); } }
        public void GoHome() {
            working = true;
            axMintController1.set_Home(0, 2);
            while (axMintController1.get_AxisMode(0) != 0) { }
            axMintController1.set_Home(1, 2);
            axMintController1.set_Home(2, 2);
            while (axMintController1.get_AxisMode(1) != 0) { }
            axMintController1.set_MoveA(1, -88181);
            while (axMintController1.get_AxisMode(1) != 0) { }
            working = false; }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (comboBox1.SelectedItem.ToString() == "From conveyor")
            {
                comboBox4.Enabled = true;
                comboBox5.Enabled = true;
                comboBox2.Enabled = false;
                comboBox3.Enabled = false;
                comboBox6.Enabled = false;
            }
            else if (comboBox1.SelectedItem.ToString() == "To conveyor")
            {
                comboBox2.Enabled = true;
                comboBox3.Enabled = true;
                comboBox4.Enabled = false;
                comboBox5.Enabled = false;

            }
            else if (comboBox1.SelectedItem.ToString() == "Empty")
            {
                comboBox2.Enabled = true;
                comboBox3.Enabled = true;
                comboBox4.Enabled = true;
                comboBox5.Enabled = true;
                comboBox6.Enabled = true;
            }
        }
        public bool validation(string payload) {
            try {
                if (payload == "take" || payload == "not found"
                    || payload == "ok" || payload == "incorrect") { return true; }
                int[] values = { 1, 2, 3, 4, 5 };
                string[] commands = payload.Split(' '); // скоп сделать общим на класс, в других функциях не видно
                if (commands[0] == "column" && values.Contains(int.Parse(commands[1]))
                && commands[2] == "row" && values.Contains(int.Parse(commands[3]))
                && commands[4] == "id" && (int.Parse(commands[5]) > 0)) { return true; }
                else { return false; } }
            catch { return false; }

        }
        // сначала всегда пишем столбец, потом строку
        public void Movement(string conveyor = "Empty", int column1 = 0, int row1 = 0,
            int column2 = 0, int row2 = 0, string pillar = "Left")
        {
            working = true;

            try
            {
                switch (conveyor)
                {
                    case "From conveyor":
                        axMintController1.set_MoveA(0, -495990);
                        axMintController1.set_MoveA(2, -130987);
                        while ((axMintController1.get_AxisMode(0) + axMintController1.get_AxisMode(2)) != 0) { }
                        axMintController1.set_MoveA(2, -144987);
                        while (axMintController1.get_AxisMode(2) != 0) { }
                        Task.Delay(10000).GetAwaiter().GetResult();
                        axMintController1.set_MoveA(2, -131987);
                        while (axMintController1.get_AxisMode(2) != 0) { }
                        axMintController1.set_MoveA(0, -148989 - 51750 * (column2 - 1));
                        while (axMintController1.get_AxisMode(0) != 0) { }
                        axMintController1.set_MoveA(2, -23987 - 38997 * (row2 - 1) + 2400);
                        while (axMintController1.get_AxisMode(2) != 0) { }
                        axMintController1.set_MoveA(1, -39150);
                        while (axMintController1.get_AxisMode(1) != 0) { }
                        axMintController1.set_MoveA(2, -23987 - 38997 * (row2 - 1) - 2400);
                        while (axMintController1.get_AxisMode(2) != 0) { }
                        axMintController1.set_MoveA(1, -88181);
                        while (axMintController1.get_AxisMode(1) != 0) { }
                        break;
                    case "To conveyor":
                        axMintController1.set_MoveA(0, -148989 - 51750 * (column1 - 1));
                        while (axMintController1.get_AxisMode(0) != 0) { }
                        axMintController1.set_MoveA(2, -23987 - 38997 * (row1 - 1) - 2400);
                        while (axMintController1.get_AxisMode(2) != 0) { }
                        axMintController1.set_MoveA(1, -136189);
                        while (axMintController1.get_AxisMode(1) != 0) { }
                        axMintController1.set_MoveA(2, -23987 - 38997 * (row1 - 1) + 2400);
                        while (axMintController1.get_AxisMode(2) != 0) { }
                        axMintController1.set_MoveA(1, -88181);
                        while (axMintController1.get_AxisMode(1) != 0) { }
                        axMintController1.set_MoveA(0, -495990);
                        axMintController1.set_MoveA(2, -130987);
                        while ((axMintController1.get_AxisMode(0) + axMintController1.get_AxisMode(2)) != 0) { }
                        axMintController1.set_MoveA(2, -144987);
                        while (axMintController1.get_AxisMode(2) != 0) { }
                        Task.Delay(10000).GetAwaiter().GetResult();
                        axMintController1.set_MoveA(2, -131987);
                        while (axMintController1.get_AxisMode(2) != 0) { }
                        break;
                    case "Empty":
                        if (pillar == "Left")
                        {
                            axMintController1.set_MoveA(0, -148989 - 51750 * (column1 - 1));
                            while (axMintController1.get_AxisMode(0) != 0) { }
                            axMintController1.set_MoveA(2, -23987 - 38997 * (row1 - 1) - 2400);
                            while (axMintController1.get_AxisMode(2) != 0) { }
                            axMintController1.set_MoveA(1, -39173);
                            while (axMintController1.get_AxisMode(1) != 0) { }
                            axMintController1.set_MoveA(2, -23987 - 38997 * (row1 - 1) + 2400);
                            while (axMintController1.get_AxisMode(2) != 0) { }
                            axMintController1.set_MoveA(1, -88181);
                            while (axMintController1.get_AxisMode(1) != 0) { }
                            axMintController1.set_MoveA(0, -148989 - 51750 * (column2 - 1));
                            while (axMintController1.get_AxisMode(0) != 0) { }
                            axMintController1.set_MoveA(2, -23987 - 38997 * (row2 - 1) + 2400);
                            while (axMintController1.get_AxisMode(2) != 0) { }
                            axMintController1.set_MoveA(1, -39173);
                            while (axMintController1.get_AxisMode(1) != 0) { }
                            axMintController1.set_MoveA(2, -23987 - 38997 * (row2 - 1) - 2400);
                            while (axMintController1.get_AxisMode(2) != 0) { }
                            axMintController1.set_MoveA(1, -88181);
                            while (axMintController1.get_AxisMode(1) != 0) { }
                        }
                        else if (pillar == "Right")
                        {
                            axMintController1.set_MoveA(0, -148989 - 51750 * (column1 - 1));
                            while (axMintController1.get_AxisMode(0) != 0) { }
                            axMintController1.set_MoveA(2, -23987 - 38997 * (row1 - 1) - 2400);
                            while (axMintController1.get_AxisMode(2) != 0) { }
                            axMintController1.set_MoveA(1, -136189);
                            while (axMintController1.get_AxisMode(1) != 0) { }
                            axMintController1.set_MoveA(2, -23987 - 38997 * (row1 - 1) + 2400);
                            while (axMintController1.get_AxisMode(2) != 0) { }
                            axMintController1.set_MoveA(1, -88181);
                            while (axMintController1.get_AxisMode(1) != 0) { }
                            axMintController1.set_MoveA(0, -148989 - 51750 * (column2 - 1));
                            while (axMintController1.get_AxisMode(0) != 0) { }
                            axMintController1.set_MoveA(2, -23987 - 38997 * (row2 - 1) + 2400);
                            while (axMintController1.get_AxisMode(2) != 0) { }
                            axMintController1.set_MoveA(1, -137189);
                            while (axMintController1.get_AxisMode(1) != 0) { }
                            axMintController1.set_MoveA(2, -23987 - 38997 * (row2 - 1) - 2400);
                            while (axMintController1.get_AxisMode(2) != 0) { }
                            axMintController1.set_MoveA(1, -88181);
                            while (axMintController1.get_AxisMode(1) != 0) { }
                        }
                        break;
                }
            }
            catch
            {
                working = false;
            }
            finally
            {
                working = false;
            }

        }

        async public void button13_Click(object sender, EventArgs e)
        {
            string conveyor = comboBox1.SelectedItem.ToString();
            int column1 = Convert.ToInt32(comboBox2.SelectedItem);
            int row1 = Convert.ToInt32(comboBox3.SelectedItem);
            int column2 = Convert.ToInt32(comboBox4.SelectedItem);
            int row2 = Convert.ToInt32(comboBox5.SelectedItem);
            string pillar = "";
            if (comboBox6.SelectedItem != null)
            {
                pillar = comboBox6.SelectedItem.ToString();
            }
            if (working) { return; }
            await Task.Run(() => Movement(conveyor, column1, row1, column2, row2, pillar));
        }

        private void comboBox2_SelectedIndexChanged(object sender, EventArgs e) { }

        private void comboBox3_SelectedIndexChanged(object sender, EventArgs e) { }

        private void comboBox4_SelectedIndexChanged(object sender, EventArgs e) { }

        private void comboBox5_SelectedIndexChanged(object sender, EventArgs e) { }

        private void comboBox6_SelectedIndexChanged(object sender, EventArgs e) { }

        private void label2_Click(object sender, EventArgs e) { }

        private void label4_Click(object sender, EventArgs e) { }

        private void label5_Click(object sender, EventArgs e) { }

        private void comboBox7_SelectedIndexChanged(object sender, EventArgs e) { }

        private void label8_Click(object sender, EventArgs e) { }

        private void button1_Click(object sender, EventArgs e) {
            short axis = short.Parse(comboBox7.SelectedItem.ToString());
            float value = float.Parse(comboBox8.SelectedItem.ToString());
            axMintController1.set_Speed(axis, value); }

        private void comboBox8_SelectedIndexChanged(object sender, EventArgs e) { }

        private void button11_Click(object sender, EventArgs e)
        {
            if (!isconnected)
            {
                devClient.Start(DeviceID, DevicePassword);
                devClient.SubscribedData += DataHandler;
                if (!devClient.WaitConnected()) { return; }
                devClient.Subscribe(topic, MQTTnet.Protocol.MqttQualityOfServiceLevel.AtLeastOnce).Wait();
                isconnected = true;
                autonomus = true;
            }

        }
        async public void DataHandler(string topic, byte[] payload) {
            recieved_data = System.Text.Encoding.UTF8.GetString(payload);
            if (!validation(recieved_data)) { return; }
            if (recieved_data == "take")
            {
                q_from_conveyor.Enqueue(recieved_data);
                if (!auto) { await Task.Run(() => auto_mode()); }
            }
            else if (recieved_data == "ok" || recieved_data == "not found"
                || recieved_data == "incorrect")
            {
                q_from_reader.Enqueue(recieved_data);
                if (!auto) { await Task.Run(() => auto_mode()); }
            }
            else
            {
                q_from_cloud.Enqueue(recieved_data);
                if (!auto) { await Task.Run(() => auto_mode()); }
            } }

        public void auto_move_to_conveyor(int column, int row, int id){
            working = true;
            String data_to_send = "run id " + id.ToString();
            axMintController1.set_MoveA(0, -148989 - 51750 * (column - 1));
            while (axMintController1.get_AxisMode(0) != 0) { }
            axMintController1.set_MoveA(2, -23987 - 38997 * (row - 1) - 2400);
            while (axMintController1.get_AxisMode(2) != 0) { }
            axMintController1.set_MoveA(1, -136189);
            while (axMintController1.get_AxisMode(1) != 0) { }
            axMintController1.set_MoveA(2, -23987 - 38997 * (row - 1) + 2400);
            while (axMintController1.get_AxisMode(2) != 0) { }
            devClient.Publish(test_topic, data_to_send, MQTTnet.Protocol.MqttQualityOfServiceLevel.AtLeastOnce); // топик тестовый, пиши здесь топик ридера
            Task.Delay(10000).GetAwaiter().GetResult();
            if (q_from_reader.Any() && q_from_reader.Dequeue() == "ok"){
                axMintController1.set_MoveA(1, -88181);
                while (axMintController1.get_AxisMode(1) != 0) { }
                axMintController1.set_MoveA(0, -495990);
                axMintController1.set_MoveA(2, -130987);
                while ((axMintController1.get_AxisMode(0) + axMintController1.get_AxisMode(2)) != 0) { }
                axMintController1.set_MoveA(2, -144987);
                while (axMintController1.get_AxisMode(2) != 0) { }
                Task.Delay(10000).GetAwaiter().GetResult();
                axMintController1.set_MoveA(2, -131987);
                while (axMintController1.get_AxisMode(2) != 0) { }
                working = false;
            }
            else{
                axMintController1.set_MoveA(2, -23987 - 38997 * (row - 1) - 2400);
                while (axMintController1.get_AxisMode(2) != 0) { }
                axMintController1.set_MoveA(1, -88181);
                working = false;
            }

        }
        public void auto_move_from_conveyor(int row, int column)
        {
            working = true;
            devClient.Publish(test_topic, "busy", MQTTnet.Protocol.MqttQualityOfServiceLevel.AtLeastOnce);
            axMintController1.set_MoveA(0, -495990);
            axMintController1.set_MoveA(2, -130987);
            while ((axMintController1.get_AxisMode(0) + axMintController1.get_AxisMode(2)) != 0) { }
            axMintController1.set_MoveA(2, -144987);
            while (axMintController1.get_AxisMode(2) != 0) { }
            devClient.Publish(test_topic, "open", MQTTnet.Protocol.MqttQualityOfServiceLevel.AtLeastOnce);
            Task.Delay(10000).GetAwaiter().GetResult();
            axMintController1.set_MoveA(2, -131987);
            while (axMintController1.get_AxisMode(2) != 0) { }
            axMintController1.set_MoveA(0, -148989 - 51750 * (column - 1));
            while (axMintController1.get_AxisMode(0) != 0) { }
            axMintController1.set_MoveA(2, -23987 - 38997 * (row - 1) + 2400);
            while (axMintController1.get_AxisMode(2) != 0) { }
            axMintController1.set_MoveA(1, -39150);
            while (axMintController1.get_AxisMode(1) != 0) { }
            axMintController1.set_MoveA(2, -23987 - 38997 * (row - 1) - 2400);
            while (axMintController1.get_AxisMode(2) != 0) { }
            axMintController1.set_MoveA(1, -88181);
            while (axMintController1.get_AxisMode(1) != 0) { }
            working = false;
            String new_coords = "column " + column + " row " + row;
            devClient.Publish(test_topic, "not busy", MQTTnet.Protocol.MqttQualityOfServiceLevel.AtLeastOnce);
            devClient.Publish(test_topic, new_coords, MQTTnet.Protocol.MqttQualityOfServiceLevel.AtLeastOnce);
        }

        async void auto_mode()
        {
            while (autonomus)
            {
                try // иногда происходит изменение очереди в момент чтения -> все падает
                    // здесь же просто пробросит исключение и заново в цикле чекнет очередь
                    // в конечном счете коллизии не будет
                {
                    auto = true;
                    if (q_from_conveyor.Any() && !working)
                    {   
                        q_from_conveyor.Dequeue();
                        int row = row_counter;
                        int column = column_counter;
                        // функция перемещения от конвейера до свободной ячейки
                        await Task.Run(() => auto_move_from_conveyor(row, column));
                        if (row_counter == 5){
                            row_counter = 1;
                            column_counter++;}
                        else { if (row_counter != 5) { row_counter++; } }
                    }
                    if (q_from_cloud.Any() && !working)
                    {
                        String[] prms = q_from_cloud.Dequeue().Split(' '); // сплит строки из очереди
                        int column = int.Parse(prms[1]); // парсинг столбца и строки
                        int row = int.Parse(prms[3]);
                        int id = int.Parse(prms[5]);
                        await Task.Run(() => auto_move_to_conveyor(column, row, id));
                    }
                }
                catch { }
            }
            auto = false;
        }
        public void label11_Click(object sender, EventArgs e){label11.Text = recieved_data;}
        private void button12_Click(object sender, EventArgs e){
            if (isconnected){
                string payload = textBox1.Text;
                // ниже строка для теста rfid ридера
                //devClient.Publish("$devices/areslq41mged71mcd3be/events/test", payload, MQTTnet.Protocol.MqttQualityOfServiceLevel.AtLeastOnce);
                // cтрока для теста склада
                devClient.Publish(test_topic, payload, MQTTnet.Protocol.MqttQualityOfServiceLevel.AtLeastOnce);} }

        private void button2_Click_1(object sender, EventArgs e){
            devClient.Stop();
            isconnected = false;
            autonomus = false;}

        private void textBox1_TextChanged(object sender, EventArgs e){}
      
        private void label12_Click(object sender, EventArgs e){}
    
        private void label13_Click(object sender, EventArgs e){}

        private void button14_Click(object sender, EventArgs e){
            if (axMintController1.get_DriveEnable(0) || axMintController1.get_DriveEnable(1)
                || axMintController1.get_DriveEnable(2) == true){
                    axMintController1.set_DriveEnable(0, false);
                    axMintController1.set_DriveEnable(1, false);
                    axMintController1.set_DriveEnable(2, false);} }

        private void label16_Click(object sender, EventArgs e){
            if (axMintController1.get_DriveEnable(0) && axMintController1.get_DriveEnable(1)
                && axMintController1.get_DriveEnable(2) == true) { label16.Text = "Drivers state: ON"; }
            else { label16.Text = "Drivers state: OFF";} }

        private void label17_Click(object sender, EventArgs e){
            if (isconnected){label17.Text = "Connection: " + isconnected;}
            else if (!isconnected){label17.Text = "Connection: " + isconnected;} }
    }
}
