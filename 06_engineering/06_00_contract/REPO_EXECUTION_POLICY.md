# Repo Execution Policy

## Core Rules
- One stage = one branch = one report.
- No direct commits to `main`.
- Stage reports must be updated incrementally, not rewritten from scratch without cause.
- Implementation evidence must be kept separate from legacy, academic, and reference materials.
- No silent scope creep.
- No claims in VKR without evidence.

## Repository Discipline
- Archive zones such as `03_nirs`, `04_vkr`, `05_sources`, and other historical materials must not be aggressively reorganized during implementation stages.
- New implementation artifacts must be placed in the active engineering and reporting zones.
- Reports must explicitly distinguish VERIFIED, INFERRED, NOT VERIFIED, and MISSING where relevant.
- Implementation progress must be traceable through files, commits, and validation notes.

## Reporting Discipline
- Every active stage must have a maintained stage report.
- The master execution report must reflect the current branch, latest commit, stage status, blockers, and open questions.
- Evidence references must point to concrete files, logs, screenshots, configs, or reproducible commands.

## Scope Discipline
- If an item is not part of approved MVP scope, it must not enter implementation by default.
- New scope must be frozen explicitly before execution expands.
- ROS 2, Gazebo, CV, SLAM, fleet management, and digital twin overengineering are forbidden in MVP unless scope is formally changed later.

## Git Discipline
- Work only in the branch assigned to the current stage.
- Commits must be meaningful and stage-specific.
- Unrelated legacy or archival changes must not be mixed into a stage commit.
