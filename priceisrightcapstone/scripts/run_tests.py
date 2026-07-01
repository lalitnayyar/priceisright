import pytest
import datetime
import os

def run():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"tests/reports/test_report_{timestamp}.md"
    
    os.makedirs("tests/reports", exist_ok=True)
    
    # We use a custom plugin to generate the markdown report
    class MarkdownReporter:
        def __init__(self, filename):
            self.filename = filename
            self.passed = 0
            self.failed = 0
            self.total = 0
            
        def pytest_runtest_logreport(self, report):
            if report.when == "call":
                self.total += 1
                if report.passed:
                    self.passed += 1
                elif report.failed:
                    self.failed += 1
                    
        def pytest_sessionfinish(self, session, exitstatus):
            with open(self.filename, "w") as f:
                f.write(f"# Test Report - {timestamp}\\n\\n")
                f.write(f"**Total Tests:** {self.total}\\n")
                f.write(f"**Passed:** {self.passed}\\n")
                f.write(f"**Failed:** {self.failed}\\n\\n")
                f.write("## Disclaimer\\n")
                f.write("Lalit Nayyar | lalitnayyar@gmail.com | +971508320336 | +919595353336\\n")
                
    pytest.main(["tests/"], plugins=[MarkdownReporter(report_file)])
    print(f"Test report generated: {report_file}")

if __name__ == "__main__":
    run()
