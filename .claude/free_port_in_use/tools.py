import platform
import subprocess
from typing import List, Dict
from helpers import _get_processes_linux, _get_processes_macos, _get_processes_windows

def list_process_ids(port_no: int) -> List[Dict[str, str]]:
    """
    Find processes running on the specified port number.
    
    Args:
        port_no: The port number to check
        
    Returns:
        List of dictionaries containing process information.
        Each dictionary has keys: 'pid', 'name', 'command'
        Returns empty list if no processes found or on error.
    """
    os_name = platform.system().lower()
    processes = []
    
    try:
        if os_name == 'linux':
            processes = _get_processes_linux(port_no)
        elif os_name == 'darwin':  # macOS
            processes = _get_processes_macos(port_no)
        elif os_name == 'windows':
            processes = _get_processes_windows(port_no)
        else:
            print(f"Unsupported operating system: {os_name}")
            return []
            
    except Exception as e:
        print(f"Error finding processes on port {port_no}: {e}")
        return []
    
    return processes

def kill_process_ids(process_ids: List[str]) -> Dict[str, any]:
    """
    Kill processes by their process IDs.
    
    Args:
        process_ids: List of process ID strings to kill
        
    Returns:
        Dictionary with 'killed' (list of successfully killed PIDs),
        'failed' (list of PIDs that failed to kill), and 'errors' (list of error messages)
    """
    os_name = platform.system().lower()
    killed = []
    failed = []
    errors = []
    
    if not process_ids:
        return {'killed': [], 'failed': [], 'errors': []}
    
    for pid in process_ids:
        try:
            if os_name == 'windows':
                subprocess.run(['taskkill', '/F', '/PID', pid], 
                             capture_output=True, check=True)
            else:  # Linux and macOS
                subprocess.run(['kill', '-9', pid], 
                             capture_output=True, check=True)
            killed.append(pid)
        except subprocess.CalledProcessError as e:
            failed.append(pid)
            errors.append(f"Failed to kill process {pid}: {e}")
        except Exception as e:
            failed.append(pid)
            errors.append(f"Error killing process {pid}: {e}")
    
    return {
        'killed': killed,
        'failed': failed,
        'errors': errors
    }
