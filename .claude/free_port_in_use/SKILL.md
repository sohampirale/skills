---
name: name
description: “Find out process id of processes consuming desired port no and kill those processes,Use this skill when we need to free up a desired port no that is occupied by a process, or when user request to free up <xyz> port or on error `port is already in use` when starting a new process”
---

# Purpose
- If desired port for new process to start is occupied/already in use due to 
  i.force stopping old process (cntl+z) without proper realease of resources such as port no
  ii.backgroud processes running that occupy the desired port
-Find out process id's of running processes on a desirec port no & kill those processes with process id received

## Variables

KILL_PROCESSES : True 

## Instructions

- Read workflow steps clearly
- Do not interfere with any `port_no` that isn't requested
- Do NOT assume any `port_no` on your own
- Do not kill processes of browser visiting a port
- NO need to read the `.claude/free_port_in_use/helpers.py` file

## Workflow

- 1. Understand clearly the EXACT `port_no` that needs to be freed
- 2. Read `.claude/free_port_in_use/tools.py` file
- 3. Use  `.claude/free_port_in_use/tools.py: def list_process_ids(port_nod)` tool to get all process ids 
- 4. Use  `.claude/free_port_in_use/tools.py: def kill_process_ids(process_ids:list[...])` tool to kill all processes using desired `port_no`
- 5. Respond with clear summary of work done
