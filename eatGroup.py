import flet as ft

TUITION_RATE = 459.54
LAB_FEE_PER_SUBJECT = 3429.30
HANDS_ON_FEE_PER_SUBJECT = 2341.86
MIN_DOWN_PAYMENT = 3500.00
EXAM_PAYMENTS = [
    ("1st Prelim", 0.15), ("1st Grading", 0.25),
    ("2nd Prelim", 0.15), ("Midterm", 0.30), ("Finals", 0.15),
]
ORANGE, INK, MUTED = "#F58220", "#292929", "#6B7280"
PALE_ORANGE, BORDER = "#FFF3E8", "#F0D8C5"

def peso(value):
    return f"₱{value:,.2f}"

def main(page: ft.Page):
    page.title = "BCT Tuition Calculator"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ORANGE)
    page.bgcolor = "#FFFFFF"
    page.padding = 0
    page.spacing = 0
    page.scroll = ft.ScrollMode.AUTO
    page.window.width, page.window.height = 390, 844
    page.window.min_width, page.window.min_height = 320, 600

    units = ft.TextField(label="Total units enrolled", hint_text="Enter 10–25",
        keyboard_type=ft.KeyboardType.NUMBER, prefix_icon=ft.Icons.MENU_BOOK,
        border_color=BORDER, focused_border_color=ORANGE, border_radius=12,
        filled=True, bgcolor="#FFFFFF", text_size=15)
    labs = ft.TextField(label="Subjects with laboratory", hint_text="Enter 1–5",
        keyboard_type=ft.KeyboardType.NUMBER, prefix_icon=ft.Icons.SCIENCE,
        border_color=BORDER, focused_border_color=ORANGE, border_radius=12,
        filled=True, bgcolor="#FFFFFF", text_size=15)
    hands = ft.TextField(label="Hands-on subjects", hint_text="Enter 1–5",
        keyboard_type=ft.KeyboardType.NUMBER, prefix_icon=ft.Icons.COMPUTER,
        border_color=BORDER, focused_border_color=ORANGE, border_radius=12,
        filled=True, bgcolor="#FFFFFF", text_size=15)
    status = ft.Text(size=13)
    result_area = ft.Column(spacing=12, visible=False)

    def row(label, amount, bold=False):
        return ft.Row([
            ft.Text(label, expand=True, size=14, color=INK,
                weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL),
            ft.Text(peso(amount), size=14, color=INK,
                weight=ft.FontWeight.BOLD if bold else ft.FontWeight.W_500),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
           vertical_alignment=ft.CrossAxisAlignment.START)

    def calculate(e):
        status.value = ""
        status.color = "#C62828"
        result_area.visible = False
        try:
            u = int(units.value.strip())
            l = int(labs.value.strip())
            h = int(hands.value.strip())
        except (ValueError, AttributeError):
            status.value = "Please enter whole numbers in all fields."
            page.update()
            return

        if not 1 <= u <= 25:
            status.value = "Units must be between 1 and 25."
        elif u < 10:
            status.value = "Error: You must enroll in at least 10 units."
        elif not 1 <= l <= 5:
            status.value = "Laboratory subjects must be from 1 to 5."
        elif not 1 <= h <= 5:
            status.value = "Hands-on subjects must be from 1 to 5."
        elif l > u or h > u:
            status.value = "LAB or hands-on subjects cannot exceed total units."
        else:
            tuition = u * TUITION_RATE
            lab_fee = l * LAB_FEE_PER_SUBJECT
            hands_fee = h * HANDS_ON_FEE_PER_SUBJECT
            total = tuition + lab_fee + hands_fee
            down = min(MIN_DOWN_PAYMENT, total)
            balance = total - down
            assessment = [
                row("Tuition fee", tuition),
                row(f"Laboratory fee · {l} subject(s)", lab_fee),
                row(f"Hands-on fee · {h} subject(s)", hands_fee),
                ft.Divider(color=BORDER, height=18),
                row("TOTAL ASSESSMENT", total, True),
            ]
            breakdown = [
                row("Down payment", down, True),
                row("Remaining balance", balance),
                ft.Divider(color=BORDER, height=18),
            ]
            breakdown.extend(row(f"{name} · {pct:.0%}", balance * pct)
                             for name, pct in EXAM_PAYMENTS)
            result_area.controls = [
                ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.RECEIPT_LONG, color=ORANGE, size=22),
                        ft.Text("Assessment", size=19, weight=ft.FontWeight.BOLD, color=INK)], spacing=8),
                    *assessment,
                ], spacing=12), bgcolor="#FFFFFF", border=ft.border.all(1, BORDER),
                    border_radius=16, padding=18),
                ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.CALENDAR_MONTH, color=ORANGE, size=22),
                        ft.Text("Payment Breakdown", size=19, weight=ft.FontWeight.BOLD, color=INK)], spacing=8),
                    *breakdown,
                ], spacing=12), bgcolor="#FFFFFF", border=ft.border.all(1, BORDER),
                    border_radius=16, padding=18),
                ft.Text("Only the tuition, laboratory, and hands-on fees specified in the project are included.",
                    size=11, color=MUTED, italic=True),
            ]
            result_area.visible = True
            status.value = "Assessment calculated successfully."
            status.color = "#27834A"
        page.update()

    def clear(e):
        units.value = labs.value = hands.value = ""
        status.value = ""
        result_area.visible = False
        page.update()

    header = ft.Container(content=ft.Column([
        ft.Image(src="bctLogos.png", width=104, height=104, fit=ft.ImageFit.CONTAIN),
        ft.Text("TUITION FEE CALCULATOR", size=20, weight=ft.FontWeight.BOLD,
            color="#FFFFFF", text_align=ft.TextAlign.CENTER),
        ft.Text("BAGUIO COLLEGE OF TECHNOLOGY", size=11, weight=ft.FontWeight.W_500,
            color="#FFF5EC", text_align=ft.TextAlign.CENTER),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
        bgcolor=ORANGE, padding=ft.padding.only(left=22, right=22, top=22, bottom=24),
        border_radius=ft.border_radius.only(bottom_left=24, bottom_right=24))

    form_card = ft.Container(content=ft.Column([
        ft.Text("Enrollment Details", size=19, weight=ft.FontWeight.BOLD, color=INK),
        ft.Text("Fill in your current enrollment information.", size=12, color=MUTED),
        units, labs, hands,
        ft.Row([
            ft.ElevatedButton("Calculate", icon=ft.Icons.CALCULATE, on_click=calculate,
                bgcolor=ORANGE, color="#FFFFFF", expand=True,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), padding=16)),
            ft.OutlinedButton("Clear", on_click=clear,
                style=ft.ButtonStyle(color=ORANGE, side=ft.BorderSide(1, ORANGE),
                    shape=ft.RoundedRectangleBorder(radius=12), padding=16)),
        ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        status,
    ], spacing=14), bgcolor=PALE_ORANGE, border_radius=16, padding=18,
        margin=ft.margin.only(left=16, right=16, top=18, bottom=16))

    page.add(ft.Column([
        header,
        form_card,
        ft.Container(content=result_area, padding=ft.padding.only(left=16, right=16, bottom=24)),
        ft.Container(content=ft.Text("BCT • Student Assessment", size=11, color=MUTED),
            alignment=ft.alignment.center, padding=ft.padding.only(bottom=16)),
    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH))

if __name__ == "__main__":
    ft.app(target=main, assets_dir=".")
