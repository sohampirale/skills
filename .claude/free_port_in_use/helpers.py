import subprocess
import re
from typing import List, Dict

def _get_processes_linux(port_no: int) -> List[Dict[str, str]]:
    """Get processes on Linux using lsof or ss/netstat."""
    processes = []
    
    # Try lsof first (most reliable)
    try:
        result = subprocess.run(
            ['lsof', '-i', f':{port_no}'],
            capture_output=True,
            text=True,
            check=True
        )
        
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:  # Skip header line
            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 2:
                    pid = parts[1]
                    name = parts[0] if len(parts) > 0 else 'unknown'
                    command = ' '.join(parts[8:]) if len(parts) > 8 else name
                    processes.append({
                        'pid': pid,
                        'name': name,
                        'command': command
                    })
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to ss command
        try:
            result = subprocess.run(
                ['ss', '-tlnp'],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.split('\n'):
                if f':{port_no}' in line:
                    # Extract PID from line like: LISTEN 0 128 *:8080 *:* users:(("python",pid=12345,fd=3))
                    pid_match = re.search(r'pid=(\d+)', line)
                    name_match = re.search(r'\((".*?"|.*?),pid=', line)
                    
                    if pid_match:
                        pid = pid_match.group(1)
                        name = name_match.group(1).strip('"') if name_match else 'unknown'
                        processes.append({
                            'pid': pid,
                            'name': name,
                            'command': name
                        })
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Last fallback to netstat
            try:
                result = subprocess.run(
                    ['netstat', '-tlnp'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                for line in result.stdout.split('\n'):
                    if f':{port_no}' in line:
                        parts = line.split()
                        if len(parts) >= 7:
                            pid_program = parts[6].split('/')
                            if len(pid_program) >= 2:
                                pid = pid_program[0]
                                name = pid_program[1]
                                processes.append({
                                    'pid': pid,
                                    'name': name,
                                    'command': name
                                })
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
    
    return processes

def _get_processes_macos(port_no: int) -> List[Dict[str, str]]:
    """Get processes on macOS using lsof."""
    processes = []
    
    try:
        result = subprocess.run(
            ['lsof', '-i', f':{port_no}'],
            capture_output=True,
            text=True,
            check=True
        )
        
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:  # Skip header line
            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 2:
                    pid = parts[1]
                    name = parts[0] if len(parts) > 0 else 'unknown'
                    command = ' '.join(parts[8:]) if len(parts) > 8 else name
                    processes.append({
                        'pid': pid,
                        'name': name,
                        'command': command
                    })
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    return processes

def _get_processes_windows(port_no: int) -> List[Dict[str, str]]:
    """Get processes on Windows using netstat."""
    processes = []
    
    try:
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True,
            check=True
        )
        
        for line in result.stdout.split('\n'):
            if f':{port_no}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    # Get process name using tasklist
                    try:
                        task_result = subprocess.run(
                            ['tasklist', '/FI', f'PID eq {pid}', '/FO', 'CSV', '/NH'],
                            capture_output=True,
                            text=True,
                            check=True
                        )
                        if task_result.stdout:
                            # CSV format: "name","pid","session","mem"
                            name_match = re.search(r'"([^"]+)"', task_result.stdout)
                            name = name_match.group(1) if name_match else 'unknown'
                        else:
                            name = 'unknown'
                    except:
                        name = 'unknown'
                    
                    processes.append({
                        'pid': pid,
                        'name': name,
                        'command': name
                    })
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    return processes
