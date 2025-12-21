
namespace Warehouse
{
    partial class Form1
    {
        /// <summary>
        /// Обязательная переменная конструктора.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Освободить все используемые ресурсы.
        /// </summary>
        /// <param name="disposing">истинно, если управляемый ресурс должен быть удален; иначе ложно.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Код, автоматически созданный конструктором форм Windows

        /// <summary>
        /// Требуемый метод для поддержки конструктора — не изменяйте 
        /// содержимое этого метода с помощью редактора кода.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.axMintController1 = new AxMintControls5513Lib.AxMintController();
            this.button3 = new System.Windows.Forms.Button();
            this.button4 = new System.Windows.Forms.Button();
            this.button5 = new System.Windows.Forms.Button();
            this.button6 = new System.Windows.Forms.Button();
            this.button7 = new System.Windows.Forms.Button();
            this.button8 = new System.Windows.Forms.Button();
            this.button9 = new System.Windows.Forms.Button();
            this.button10 = new System.Windows.Forms.Button();
            this.comboBox1 = new System.Windows.Forms.ComboBox();
            this.button13 = new System.Windows.Forms.Button();
            this.comboBox2 = new System.Windows.Forms.ComboBox();
            this.comboBox3 = new System.Windows.Forms.ComboBox();
            this.comboBox4 = new System.Windows.Forms.ComboBox();
            this.comboBox5 = new System.Windows.Forms.ComboBox();
            this.comboBox6 = new System.Windows.Forms.ComboBox();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.comboBox7 = new System.Windows.Forms.ComboBox();
            this.comboBox8 = new System.Windows.Forms.ComboBox();
            this.label8 = new System.Windows.Forms.Label();
            this.label9 = new System.Windows.Forms.Label();
            this.label10 = new System.Windows.Forms.Label();
            this.button1 = new System.Windows.Forms.Button();
            this.button11 = new System.Windows.Forms.Button();
            this.label11 = new System.Windows.Forms.Label();
            this.button12 = new System.Windows.Forms.Button();
            this.button2 = new System.Windows.Forms.Button();
            this.textBox1 = new System.Windows.Forms.TextBox();
            this.label12 = new System.Windows.Forms.Label();
            this.label13 = new System.Windows.Forms.Label();
            this.button14 = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.label14 = new System.Windows.Forms.Label();
            this.label15 = new System.Windows.Forms.Label();
            this.label16 = new System.Windows.Forms.Label();
            this.label17 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.axMintController1)).BeginInit();
            this.SuspendLayout();
            // 
            // axMintController1
            // 
            this.axMintController1.Enabled = true;
            this.axMintController1.Location = new System.Drawing.Point(706, 126);
            this.axMintController1.Name = "axMintController1";
            this.axMintController1.OcxState = ((System.Windows.Forms.AxHost.State)(resources.GetObject("axMintController1.OcxState")));
            this.axMintController1.Size = new System.Drawing.Size(28, 28);
            this.axMintController1.TabIndex = 0;
            this.axMintController1.SerialReceiveEvent += new System.EventHandler(this.axMintController1_SerialReceiveEvent);
            // 
            // button3
            // 
            this.button3.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.button3.Location = new System.Drawing.Point(871, 105);
            this.button3.Name = "button3";
            this.button3.Size = new System.Drawing.Size(100, 70);
            this.button3.TabIndex = 3;
            this.button3.Text = "X+";
            this.button3.UseVisualStyleBackColor = true;
            this.button3.Click += new System.EventHandler(this.button3_Click);
            // 
            // button4
            // 
            this.button4.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.button4.Location = new System.Drawing.Point(1021, 105);
            this.button4.Name = "button4";
            this.button4.Size = new System.Drawing.Size(100, 70);
            this.button4.TabIndex = 4;
            this.button4.Text = "X-";
            this.button4.UseVisualStyleBackColor = true;
            this.button4.Click += new System.EventHandler(this.button4_Click);
            // 
            // button5
            // 
            this.button5.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.button5.Location = new System.Drawing.Point(871, 189);
            this.button5.Name = "button5";
            this.button5.Size = new System.Drawing.Size(100, 70);
            this.button5.TabIndex = 5;
            this.button5.Text = "Y+";
            this.button5.UseVisualStyleBackColor = true;
            this.button5.Click += new System.EventHandler(this.button5_Click);
            // 
            // button6
            // 
            this.button6.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.button6.Location = new System.Drawing.Point(1021, 189);
            this.button6.Name = "button6";
            this.button6.Size = new System.Drawing.Size(100, 70);
            this.button6.TabIndex = 6;
            this.button6.Text = "Y-";
            this.button6.UseVisualStyleBackColor = true;
            this.button6.Click += new System.EventHandler(this.button6_Click);
            // 
            // button7
            // 
            this.button7.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.button7.Location = new System.Drawing.Point(871, 271);
            this.button7.Name = "button7";
            this.button7.Size = new System.Drawing.Size(100, 70);
            this.button7.TabIndex = 7;
            this.button7.Text = "Z+";
            this.button7.UseVisualStyleBackColor = true;
            this.button7.Click += new System.EventHandler(this.button7_Click);
            // 
            // button8
            // 
            this.button8.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.button8.Location = new System.Drawing.Point(1021, 271);
            this.button8.Name = "button8";
            this.button8.Size = new System.Drawing.Size(100, 70);
            this.button8.TabIndex = 8;
            this.button8.Text = "Z-";
            this.button8.UseVisualStyleBackColor = true;
            this.button8.Click += new System.EventHandler(this.button8_Click);
            // 
            // button9
            // 
            this.button9.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.button9.Location = new System.Drawing.Point(12, 105);
            this.button9.Name = "button9";
            this.button9.Size = new System.Drawing.Size(400, 70);
            this.button9.TabIndex = 9;
            this.button9.Text = "Home";
            this.button9.UseVisualStyleBackColor = true;
            this.button9.Click += new System.EventHandler(this.button9_Click);
            // 
            // button10
            // 
            this.button10.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.button10.Location = new System.Drawing.Point(12, 21);
            this.button10.Name = "button10";
            this.button10.Size = new System.Drawing.Size(400, 70);
            this.button10.TabIndex = 12;
            this.button10.Text = "Drives Enable";
            this.button10.UseVisualStyleBackColor = true;
            this.button10.Click += new System.EventHandler(this.button10_Click);
            // 
            // comboBox1
            // 
            this.comboBox1.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.comboBox1.FormattingEnabled = true;
            this.comboBox1.Items.AddRange(new object[] {
            "From conveyor",
            "To conveyor",
            "Empty"});
            this.comboBox1.Location = new System.Drawing.Point(589, 14);
            this.comboBox1.Name = "comboBox1";
            this.comboBox1.Size = new System.Drawing.Size(250, 45);
            this.comboBox1.TabIndex = 17;
            this.comboBox1.SelectedIndexChanged += new System.EventHandler(this.comboBox1_SelectedIndexChanged);
            // 
            // button13
            // 
            this.button13.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.button13.Location = new System.Drawing.Point(871, 14);
            this.button13.Name = "button13";
            this.button13.Size = new System.Drawing.Size(250, 70);
            this.button13.TabIndex = 22;
            this.button13.Text = "Move";
            this.button13.UseVisualStyleBackColor = true;
            this.button13.Click += new System.EventHandler(this.button13_Click);
            // 
            // comboBox2
            // 
            this.comboBox2.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.comboBox2.FormattingEnabled = true;
            this.comboBox2.Items.AddRange(new object[] {
            "1",
            "2",
            "3",
            "4",
            "5"});
            this.comboBox2.Location = new System.Drawing.Point(589, 113);
            this.comboBox2.Name = "comboBox2";
            this.comboBox2.Size = new System.Drawing.Size(60, 45);
            this.comboBox2.TabIndex = 23;
            this.comboBox2.SelectedIndexChanged += new System.EventHandler(this.comboBox2_SelectedIndexChanged);
            // 
            // comboBox3
            // 
            this.comboBox3.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.comboBox3.FormattingEnabled = true;
            this.comboBox3.Items.AddRange(new object[] {
            "1",
            "2",
            "3",
            "4",
            "5"});
            this.comboBox3.Location = new System.Drawing.Point(779, 113);
            this.comboBox3.Name = "comboBox3";
            this.comboBox3.Size = new System.Drawing.Size(60, 45);
            this.comboBox3.TabIndex = 24;
            this.comboBox3.SelectedIndexChanged += new System.EventHandler(this.comboBox3_SelectedIndexChanged);
            // 
            // comboBox4
            // 
            this.comboBox4.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.comboBox4.FormattingEnabled = true;
            this.comboBox4.Items.AddRange(new object[] {
            "1",
            "2",
            "3",
            "4",
            "5"});
            this.comboBox4.Location = new System.Drawing.Point(589, 180);
            this.comboBox4.Name = "comboBox4";
            this.comboBox4.Size = new System.Drawing.Size(60, 45);
            this.comboBox4.TabIndex = 25;
            this.comboBox4.SelectedIndexChanged += new System.EventHandler(this.comboBox4_SelectedIndexChanged);
            // 
            // comboBox5
            // 
            this.comboBox5.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.comboBox5.FormattingEnabled = true;
            this.comboBox5.Items.AddRange(new object[] {
            "1",
            "2",
            "3",
            "4",
            "5"});
            this.comboBox5.Location = new System.Drawing.Point(779, 180);
            this.comboBox5.Name = "comboBox5";
            this.comboBox5.Size = new System.Drawing.Size(60, 45);
            this.comboBox5.TabIndex = 26;
            this.comboBox5.SelectedIndexChanged += new System.EventHandler(this.comboBox5_SelectedIndexChanged);
            // 
            // comboBox6
            // 
            this.comboBox6.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.comboBox6.FormattingEnabled = true;
            this.comboBox6.Items.AddRange(new object[] {
            "Left",
            "Right"});
            this.comboBox6.Location = new System.Drawing.Point(589, 250);
            this.comboBox6.Name = "comboBox6";
            this.comboBox6.Size = new System.Drawing.Size(120, 45);
            this.comboBox6.TabIndex = 27;
            this.comboBox6.SelectedIndexChanged += new System.EventHandler(this.comboBox6_SelectedIndexChanged);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.label2.Location = new System.Drawing.Point(428, 21);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(149, 39);
            this.label2.TabIndex = 28;
            this.label2.Text = "Conveyor";
            this.label2.Click += new System.EventHandler(this.label2_Click);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.label3.Location = new System.Drawing.Point(428, 116);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(90, 39);
            this.label3.TabIndex = 29;
            this.label3.Text = "From";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.label4.Location = new System.Drawing.Point(555, 70);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(125, 39);
            this.label4.TabIndex = 30;
            this.label4.Text = "Column";
            this.label4.Click += new System.EventHandler(this.label4_Click);
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.label5.Location = new System.Drawing.Point(766, 70);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(82, 39);
            this.label5.TabIndex = 31;
            this.label5.Text = "Row";
            this.label5.Click += new System.EventHandler(this.label5_Click);
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.label6.Location = new System.Drawing.Point(431, 180);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(53, 39);
            this.label6.TabIndex = 32;
            this.label6.Text = "To";
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.label7.Location = new System.Drawing.Point(431, 250);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(89, 39);
            this.label7.TabIndex = 33;
            this.label7.Text = "Pillar";
            // 
            // comboBox7
            // 
            this.comboBox7.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.comboBox7.FormattingEnabled = true;
            this.comboBox7.Items.AddRange(new object[] {
            "0",
            "1",
            "2"});
            this.comboBox7.Location = new System.Drawing.Point(191, 540);
            this.comboBox7.Name = "comboBox7";
            this.comboBox7.Size = new System.Drawing.Size(121, 45);
            this.comboBox7.TabIndex = 34;
            this.comboBox7.SelectedIndexChanged += new System.EventHandler(this.comboBox7_SelectedIndexChanged);
            // 
            // comboBox8
            // 
            this.comboBox8.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.comboBox8.FormattingEnabled = true;
            this.comboBox8.Items.AddRange(new object[] {
            "4000",
            "8000",
            "12000",
            "16000",
            "20000",
            "24000"});
            this.comboBox8.Location = new System.Drawing.Point(361, 540);
            this.comboBox8.Name = "comboBox8";
            this.comboBox8.Size = new System.Drawing.Size(121, 45);
            this.comboBox8.TabIndex = 35;
            this.comboBox8.SelectedIndexChanged += new System.EventHandler(this.comboBox8_SelectedIndexChanged);
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.label8.Location = new System.Drawing.Point(12, 543);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(152, 39);
            this.label8.TabIndex = 36;
            this.label8.Text = "Set Speed";
            this.label8.Click += new System.EventHandler(this.label8_Click);
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.label9.Location = new System.Drawing.Point(212, 498);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(80, 39);
            this.label9.TabIndex = 37;
            this.label9.Text = "Axis";
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.label10.Location = new System.Drawing.Point(368, 498);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(93, 39);
            this.label10.TabIndex = 38;
            this.label10.Text = "Value";
            // 
            // button1
            // 
            this.button1.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.button1.Location = new System.Drawing.Point(528, 526);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(250, 70);
            this.button1.TabIndex = 39;
            this.button1.Text = "Set Speed";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // button11
            // 
            this.button11.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.button11.Location = new System.Drawing.Point(12, 197);
            this.button11.Name = "button11";
            this.button11.Size = new System.Drawing.Size(400, 70);
            this.button11.TabIndex = 41;
            this.button11.Text = "Connect to YaCloud";
            this.button11.UseVisualStyleBackColor = true;
            this.button11.Click += new System.EventHandler(this.button11_Click);
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.label11.Location = new System.Drawing.Point(246, 385);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(114, 39);
            this.label11.TabIndex = 42;
            this.label11.Text = "label11";
            this.label11.Click += new System.EventHandler(this.label11_Click);
            // 
            // button12
            // 
            this.button12.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.button12.Location = new System.Drawing.Point(528, 422);
            this.button12.Name = "button12";
            this.button12.Size = new System.Drawing.Size(250, 70);
            this.button12.TabIndex = 43;
            this.button12.Text = "Publish";
            this.button12.UseVisualStyleBackColor = true;
            this.button12.Click += new System.EventHandler(this.button12_Click);
            // 
            // button2
            // 
            this.button2.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.button2.Location = new System.Drawing.Point(12, 291);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(400, 70);
            this.button2.TabIndex = 44;
            this.button2.Text = "Disconnect from YaCld";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Click += new System.EventHandler(this.button2_Click_1);
            // 
            // textBox1
            // 
            this.textBox1.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.textBox1.Location = new System.Drawing.Point(253, 436);
            this.textBox1.Name = "textBox1";
            this.textBox1.Size = new System.Drawing.Size(265, 46);
            this.textBox1.TabIndex = 45;
            this.textBox1.TextChanged += new System.EventHandler(this.textBox1_TextChanged);
            // 
            // label12
            // 
            this.label12.AutoSize = true;
            this.label12.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.label12.Location = new System.Drawing.Point(12, 385);
            this.label12.Name = "label12";
            this.label12.Size = new System.Drawing.Size(216, 39);
            this.label12.TabIndex = 46;
            this.label12.Text = "Recieved data:";
            this.label12.Click += new System.EventHandler(this.label12_Click);
            // 
            // label13
            // 
            this.label13.AutoSize = true;
            this.label13.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.label13.Location = new System.Drawing.Point(12, 439);
            this.label13.Name = "label13";
            this.label13.Size = new System.Drawing.Size(222, 39);
            this.label13.TabIndex = 47;
            this.label13.Text = "Published data:";
            this.label13.Click += new System.EventHandler(this.label13_Click);
            // 
            // button14
            // 
            this.button14.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.button14.Location = new System.Drawing.Point(871, 496);
            this.button14.Name = "button14";
            this.button14.Size = new System.Drawing.Size(250, 100);
            this.button14.TabIndex = 49;
            this.button14.Text = "STOP";
            this.button14.UseVisualStyleBackColor = true;
            this.button14.Click += new System.EventHandler(this.button14_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Times New Roman", 16F);
            this.label1.Location = new System.Drawing.Point(910, 385);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(82, 31);
            this.label1.TabIndex = 10;
            this.label1.Text = "label1";
            this.label1.Click += new System.EventHandler(this.label1_Click);
            // 
            // label14
            // 
            this.label14.AutoSize = true;
            this.label14.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.label14.Location = new System.Drawing.Point(864, 344);
            this.label14.Name = "label14";
            this.label14.Size = new System.Drawing.Size(227, 39);
            this.label14.TabIndex = 48;
            this.label14.Text = "Current coords:";
            // 
            // label15
            // 
            this.label15.AutoSize = true;
            this.label15.Font = new System.Drawing.Font("Times New Roman", 16F);
            this.label15.Location = new System.Drawing.Point(865, 385);
            this.label15.Name = "label15";
            this.label15.Size = new System.Drawing.Size(39, 93);
            this.label15.TabIndex = 50;
            this.label15.Text = "X:\nY:\nZ:";
            // 
            // label16
            // 
            this.label16.AutoSize = true;
            this.label16.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.label16.Location = new System.Drawing.Point(431, 322);
            this.label16.Name = "label16";
            this.label16.Size = new System.Drawing.Size(115, 39);
            this.label16.TabIndex = 51;
            this.label16.Text = "label16";
            this.label16.Click += new System.EventHandler(this.label16_Click);
            // 
            // label17
            // 
            this.label17.AutoSize = true;
            this.label17.Font = new System.Drawing.Font("Times New Roman", 20F);
            this.label17.Location = new System.Drawing.Point(534, 377);
            this.label17.Name = "label17";
            this.label17.Size = new System.Drawing.Size(115, 39);
            this.label17.TabIndex = 52;
            this.label17.Text = "label17";
            this.label17.Click += new System.EventHandler(this.label17_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1176, 639);
            this.Controls.Add(this.label17);
            this.Controls.Add(this.label16);
            this.Controls.Add(this.label15);
            this.Controls.Add(this.button14);
            this.Controls.Add(this.label14);
            this.Controls.Add(this.label13);
            this.Controls.Add(this.label12);
            this.Controls.Add(this.textBox1);
            this.Controls.Add(this.button2);
            this.Controls.Add(this.button12);
            this.Controls.Add(this.label11);
            this.Controls.Add(this.button11);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.label10);
            this.Controls.Add(this.label9);
            this.Controls.Add(this.label8);
            this.Controls.Add(this.comboBox8);
            this.Controls.Add(this.comboBox7);
            this.Controls.Add(this.label7);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.comboBox6);
            this.Controls.Add(this.comboBox5);
            this.Controls.Add(this.comboBox4);
            this.Controls.Add(this.comboBox3);
            this.Controls.Add(this.comboBox2);
            this.Controls.Add(this.button13);
            this.Controls.Add(this.comboBox1);
            this.Controls.Add(this.button10);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.button9);
            this.Controls.Add(this.button8);
            this.Controls.Add(this.button7);
            this.Controls.Add(this.button6);
            this.Controls.Add(this.button5);
            this.Controls.Add(this.button4);
            this.Controls.Add(this.button3);
            this.Controls.Add(this.axMintController1);
            this.Name = "Warehouse";
            this.Text = "Warehouse";
            this.Load += new System.EventHandler(this.Form1_Load);
            ((System.ComponentModel.ISupportInitialize)(this.axMintController1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private AxMintControls5513Lib.AxMintController axMintController1;
        private System.Windows.Forms.Button button3;
        private System.Windows.Forms.Button button4;
        private System.Windows.Forms.Button button5;
        private System.Windows.Forms.Button button6;
        private System.Windows.Forms.Button button7;
        private System.Windows.Forms.Button button8;
        private System.Windows.Forms.Button button9;
        private System.Windows.Forms.Button button10;
        private System.Windows.Forms.ComboBox comboBox1;
        private System.Windows.Forms.Button button13;
        private System.Windows.Forms.ComboBox comboBox2;
        private System.Windows.Forms.ComboBox comboBox3;
        private System.Windows.Forms.ComboBox comboBox4;
        private System.Windows.Forms.ComboBox comboBox5;
        private System.Windows.Forms.ComboBox comboBox6;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.ComboBox comboBox7;
        private System.Windows.Forms.ComboBox comboBox8;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.Button button11;
        private System.Windows.Forms.Label label11;
        private System.Windows.Forms.Button button12;
        private System.Windows.Forms.Button button2;
        private System.Windows.Forms.TextBox textBox1;
        private System.Windows.Forms.Label label12;
        private System.Windows.Forms.Label label13;
        private System.Windows.Forms.Button button14;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label14;
        private System.Windows.Forms.Label label15;
        private System.Windows.Forms.Label label16;
        private System.Windows.Forms.Label label17;
    }
}

