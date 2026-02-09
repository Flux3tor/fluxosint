from backend.engine.base import OSINTModule
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime

class Module(OSINTModule):
    name = "Report Generator"
    target_types = ["username", "email", "domain"]

    def run(self, target):
        os.makedirs("storage/reports", exist_ok=True)

        filename = f"storage/reports/{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)

        text = c.beginText(40, 800)
        text.setFont("Helvetica", 12)

        text.textLine("FluxOSINT Intelligence Report")
        text.textLine("=" * 40)
        text.textLine("")
        text.textLine(f"Target: {target}")
        text.textLine(f"Generated: {datetime.now()}")
        text.textLine("")
        text.textLine("This report summarizes publicly available intelligence")
        text.textLine("collected by FluxOSINT modules.")
        text.textLine("")
        text.textLine("Findings:")
        text.textLine("- This is an automated OSINT report.")
        text.textLine("- Data accuracy depends on public sources.")
        text.textLine("")
        text.textLine("End of Report.")

        c.drawText(text)
        c.showPage()
        c.save()

        return {
            "status": "ok",
            "data": {
                "report_file": filename
            },
            "risk": 0
        }
