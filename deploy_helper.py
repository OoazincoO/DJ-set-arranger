#!/usr/bin/env python3
"""SSH部署辅助脚本"""
import paramiko
import sys
import time

SERVER = '113.45.151.98'
USERNAME = 'root'
PASSWORD = '20070612Sb'

def run_command(command, timeout=300):
    """执行远程命令"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=15)
        stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
        out = stdout.read().decode('utf-8', errors='ignore')
        err = stderr.read().decode('utf-8', errors='ignore')
        exit_code = stdout.channel.recv_exit_status()
        client.close()
        return exit_code, out, err
    except Exception as e:
        return -1, '', str(e)

def upload_file(local_path, remote_path):
    """上传文件"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=15)
        sftp = client.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()
        client.close()
        return True
    except Exception as e:
        print(f"Upload error: {e}")
        return False

def upload_dir(local_dir, remote_dir):
    """上传目录"""
    import os
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=15)
        sftp = client.open_sftp()

        # 创建远程目录
        try:
            sftp.mkdir(remote_dir)
        except:
            pass

        for root, dirs, files in os.walk(local_dir):
            # 计算相对路径
            rel_path = os.path.relpath(root, local_dir)
            if rel_path == '.':
                remote_root = remote_dir
            else:
                remote_root = remote_dir + '/' + rel_path.replace('\\', '/')

            # 跳过不需要的目录
            if '__pycache__' in root or 'venv' in root or '.git' in root or 'node_modules' in root:
                continue

            # 创建子目录
            try:
                sftp.mkdir(remote_root)
            except:
                pass

            # 上传文件
            for f in files:
                if f.endswith('.pyc') or f.startswith('.'):
                    continue
                local_file = os.path.join(root, f)
                remote_file = remote_root + '/' + f
                try:
                    sftp.put(local_file, remote_file)
                    print(f"  Uploaded: {f}")
                except Exception as e:
                    print(f"  Failed: {f} - {e}")

        sftp.close()
        client.close()
        return True
    except Exception as e:
        print(f"Upload dir error: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python deploy_helper.py <command>")
        sys.exit(1)

    cmd = ' '.join(sys.argv[1:])
    code, out, err = run_command(cmd)
    print(out)
    if err:
        print("STDERR:", err)
    sys.exit(code)
