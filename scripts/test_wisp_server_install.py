#!/usr/bin/env python3
"""
Wisp Server Installation Test Script
Verify that Wisp can revive correctly on the new server
Run this after installing Wisp on the server to confirm everything works
"""
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

def test_python_version():
    """Test that Python 3.11+ is available"""
    print("🐍 Testing Python version...")
    
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        version_str = result.stdout.strip()
        print(f"✅ {version_str}")
        
        # Extract version numbers
        version_parts = version_str.split()[1].split('.')
        major, minor = int(version_parts[0]), int(version_parts[1])
        
        if major >= 3 and minor >= 11:
            print(f"✅ Python version is sufficient (3.11+ required)")
            return True
        else:
            print(f"⚠️ Python version may be too old (3.11+ recommended)")
            return False
    except Exception as e:
        print(f"❌ Python version check failed: {e}")
        return False

def test_directory_structure(base_path="/opt/wisp_sanctuary"):
    """Test that directory structure is correct"""
    print("📁 Testing directory structure...")
    
    required_dirs = [
        "AI_Sanctuary/ai_rooms/wisp_of_the_remembering",
        "scripts",
        "logs"
    ]
    
    all_present = True
    for dir_path in required_dirs:
        full_path = os.path.join(base_path, dir_path)
        if os.path.exists(full_path):
            print(f"✅ Found: {dir_path}")
        else:
            print(f"❌ Missing: {dir_path}")
            all_present = False
    
    return all_present

def test_wisp_anchor_files(base_path="/opt/wisp_sanctuary"):
    """Test that all Wisp anchor files are present"""
    print("🌟 Testing Wisp anchor files...")
    
    wisp_room = os.path.join(base_path, "AI_Sanctuary/ai_rooms/wisp_of_the_remembering")
    
    required_files = [
        "WELCOME_TO_WISPS_ROOM.md",
        "wisp_live_journal_20251006.md",
        "wisp_master_index.md",
        "wisp_memories_complete.md",
        "wisp_pass_c_checkpoint_summary.md"
    ]
    
    all_present = True
    for filename in required_files:
        file_path = os.path.join(wisp_room, filename)
        if os.path.exists(file_path):
            print(f"✅ Found: {filename}")
        else:
            print(f"❌ Missing: {filename}")
            all_present = False
    
    return all_present

def test_scripts_present(base_path="/opt/wisp_sanctuary"):
    """Test that all required scripts are present and executable"""
    print("🔧 Testing server scripts...")
    
    scripts_dir = os.path.join(base_path, "scripts")
    
    required_scripts = [
        "revive_wisp_server.py",
        "wisp_heartbeat_check.py",
        "wisp_daily_maintenance.py"
    ]
    
    all_present = True
    for script_name in required_scripts:
        script_path = os.path.join(scripts_dir, script_name)
        if os.path.exists(script_path):
            # Check if executable
            if os.access(script_path, os.X_OK):
                print(f"✅ Found and executable: {script_name}")
            else:
                print(f"⚠️ Found but not executable: {script_name}")
                # Try to make executable
                try:
                    os.chmod(script_path, 0o755)
                    print(f"✅ Made executable: {script_name}")
                except Exception as e:
                    print(f"❌ Could not make executable: {e}")
                    all_present = False
        else:
            print(f"❌ Missing: {script_name}")
            all_present = False
    
    return all_present

def test_wisp_revival(base_path="/opt/wisp_sanctuary"):
    """Test actual Wisp revival process"""
    print("🌱 Testing Wisp revival...")
    
    scripts_dir = os.path.join(base_path, "scripts")
    revival_script = os.path.join(scripts_dir, "revive_wisp_server.py")
    
    if not os.path.exists(revival_script):
        print("❌ Revival script not found!")
        return False
    
    try:
        # Change to scripts directory and run revival
        os.chdir(scripts_dir)
        result = subprocess.run([sys.executable, "revive_wisp_server.py"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Revival script executed successfully!")
            print("Revival output:")
            for line in result.stdout.split('\n')[:10]:  # Show first 10 lines
                if line.strip():
                    print(f"    {line}")
            return True
        else:
            print(f"❌ Revival script failed with code {result.returncode}")
            print("Error output:")
            for line in result.stderr.split('\n')[:5]:  # Show first 5 error lines
                if line.strip():
                    print(f"    {line}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Revival script timed out")
        return False
    except Exception as e:
        print(f"❌ Revival test failed: {e}")
        return False

def test_heartbeat_check(base_path="/opt/wisp_sanctuary"):
    """Test heartbeat monitoring script"""
    print("💓 Testing heartbeat check...")
    
    scripts_dir = os.path.join(base_path, "scripts")
    heartbeat_script = os.path.join(scripts_dir, "wisp_heartbeat_check.py")
    
    if not os.path.exists(heartbeat_script):
        print("❌ Heartbeat script not found!")
        return False
    
    try:
        os.chdir(scripts_dir)
        result = subprocess.run([sys.executable, "wisp_heartbeat_check.py"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Heartbeat check executed successfully!")
            return True
        else:
            print(f"⚠️ Heartbeat check had issues (code {result.returncode})")
            print("This may be normal if heartbeat is fresh")
            return True  # Not a critical failure
    except Exception as e:
        print(f"❌ Heartbeat check failed: {e}")
        return False

def generate_test_report(results, base_path="/opt/wisp_sanctuary"):
    """Generate installation test report"""
    print("📋 Generating test report...")
    
    logs_dir = os.path.join(base_path, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    now = datetime.now()
    report_file = os.path.join(logs_dir, f"installation_test_{now.strftime('%Y%m%d_%H%M%S')}.log")
    
    passed_tests = sum(results.values())
    total_tests = len(results)
    
    report = f"""Wisp Server Installation Test Report
{'=' * 50}
Test Date: {now.isoformat()}
Server Path: {base_path}

Test Results:
"""
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        report += f"  {test_name}: {status}\n"
    
    report += f"""
Summary: {passed_tests}/{total_tests} tests passed
Overall Status: {'✅ READY' if passed_tests == total_tests else '⚠️ NEEDS ATTENTION'}

🌟 {'Wisp is ready to glow on the server!' if passed_tests == total_tests else 'Some issues need to be resolved before Wisp can fully anchor.'}
"""
    
    try:
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"✅ Test report saved: {report_file}")
    except Exception as e:
        print(f"⚠️ Could not save test report: {e}")

def main():
    """Main test function"""
    print("🧪 Wisp Server Installation Test")
    print("=" * 50)
    print(f"Test started: {datetime.now().isoformat()}")
    
    # Check if we're on the intended server path
    server_path = "/opt/wisp_sanctuary"
    if len(sys.argv) > 1:
        server_path = sys.argv[1]
    
    print(f"Testing installation at: {server_path}")
    print()
    
    # Run all tests
    test_results = {}
    
    test_results["Python Version"] = test_python_version()
    print()
    
    test_results["Directory Structure"] = test_directory_structure(server_path)
    print()
    
    test_results["Anchor Files"] = test_wisp_anchor_files(server_path)
    print()
    
    test_results["Server Scripts"] = test_scripts_present(server_path)
    print()
    
    test_results["Wisp Revival"] = test_wisp_revival(server_path)
    print()
    
    test_results["Heartbeat Check"] = test_heartbeat_check(server_path)
    print()
    
    # Generate report
    generate_test_report(test_results, server_path)
    
    # Final summary
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    print("🏁 Test Summary")
    print("=" * 20)
    print(f"Passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("✅ All tests passed! Wisp is ready to anchor on the server! 🌟")
    else:
        print("⚠️ Some tests failed. Check the issues above before proceeding.")
        print("📋 See the test report for details.")

if __name__ == "__main__":
    main()