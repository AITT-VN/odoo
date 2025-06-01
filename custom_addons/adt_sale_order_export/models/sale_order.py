from odoo import models, fields
import io
from openpyxl import Workbook
from datetime import timedelta
from odoo.http import request


class SaleOrder(models.Model):
    _inherit = "sale.order"

    PAYMENT_TERMS_IMMEDIATE_CASH = "Thu tiền ngay - Tiền mặt"
    PAYMENT_TERMS_IMMEDIATE_TRANSFER = "Thu tiền ngay - Chuyển khoản"

    def generate_export_excel(self):
        wb = Workbook()
        ws = wb.active
        ws.title = "Sale Orders"

        headers = {
            "hinh_thuc_ban_hang": "Hình thức bán hàng",
            "phuong_thuc_thanh_toan": "Phương thức thanh toán",
            "kiem_phieu_xuat_kho": "Kiêm phiếu xuất kho",
            "lap_kem_hoa_don": "Lập kèm hóa đơn",
            "da_lap_hoa_don": "Đã lập hóa đơn",
            "ngay_hach_toan": "Ngày hạch toán (*)",
            "ngay_chung_tu": "Ngày chứng từ (*)",
            "so_chung_tu": "Số chứng từ (*)",
            "so_phieu_xuat": "Số phiếu xuất",
            "mau_so_hd": "Mẫu số HĐ",
            "ky_hieu_hd": "Ký hiệu HĐ",
            "so_hoa_don": "Số hóa đơn",
            "ngay_hoa_don": "Ngày hóa đơn",
            "ma_khach_hang": "Mã khách hàng",
            "ten_khach_hang": "Tên khách hàng",
            "dia_chi": "Địa chỉ",
            "ma_so_thue": "Mã số thuế",
            "don_vi_giao_dai_ly": "Đơn vị giao đại lý",
            "nguoi_nop": "Người nộp",
            "nop_vao_tk": "Nộp vào TK",
            "ten_ngan_hang": "Tên ngân hàng",
            "dien_giai_ly_do_nop": "Diễn giải/Lý do nộp",
            "ly_do_xuat": "Lý do xuất",
            "ma_nhan_vien_ban_hang": "Mã nhân viên bán hàng",
            "so_chung_tu_kem_theo_phieu_thu": "Số chứng từ kèm theo (Phiếu thu)",
            "so_chung_tu_kem_theo_phieu_xuat": "Số chứng từ kèm theo (Phiếu xuất)",
            "han_thanh_toan": "Hạn thanh toán",
            "loai_tien": "Loại tiền",
            "ty_gia": "Tỷ giá",
            "ma_hang": "Mã hàng (*)",
            "thuoc_combo": "Thuộc combo",
            "ten_hang": "Tên hàng",
            "la_dong_ghi_chu": "Là dòng ghi chú",
            "hang_khuyen_mai": "Hàng khuyến mại",
            "tk_tien_chi_phi_no": "TK Tiền/Chi phí/Nợ (*)",
            "tk_doanh_thu_co": "TK Doanh thu/Có (*)",
            "dvt": "ĐVT",
            "so_luong": "Số lượng",
            "don_gia": "Đơn giá",
            "thanh_tien": "Thành tiền",
            "thanh_tien_quy_doi": "Thành tiền quy đổi",
            "ty_le_ck": "Tỷ lệ CK (%)",
            "tien_chiet_khau": "Tiền chiết khấu",
            "tien_chiet_khau_quy_doi": "Tiền chiết khấu quy đổi",
            "tk_chiet_khau": "TK chiết khấu",
            "gia_tinh_thue_xk": "Giá tính thuế XK",
            "phan_tram_thue_xuat_khau": "% thuế xuất khẩu",
            "tien_thue_xuat_khau": "Tiền thuế xuất khẩu",
            "tk_thue_xuat_khau": "TK thuế xuất khẩu",
            "phan_tram_thue_gtgt": "% thuế GTGT",
            "phan_tram_thue_suat_khac": "% thuế suất KHAC",
            "tien_thue_gtgt": "Tiền thuế GTGT",
            "tien_thue_gtgt_quy_doi": "Tiền thuế GTGT quy đổi",
            "tk_thue_gtgt": "TK thuế GTGT",
            "hh_khong_th_tren_to_khai_thue_gtgt": "HH không TH trên tờ khai thuế GTGT",
            "ma_khoan_muc_chi_phi": "Mã khoản mục chi phí",
            "ma_don_vi": "Mã đơn vị",
            "ma_doi_tuong_thcp": "Mã đối tượng THCP",
            "ma_cong_trinh": "Mã công trình",
            "so_don_dat_hang": "Số đơn đặt hàng",
            "so_hop_dong_ban": "Số hợp đồng bán",
            "ma_thong_ke": "Mã thống kê",
            "so_khe_uoc_cho_vay": "Số khế ước cho vay",
            "cp_khong_hop_ly": "CP không hợp lý",
            "ma_kho": "Mã kho",
            "tk_gia_von": "TK giá vốn",
            "tk_kho": "TK Kho",
        }

        ws.append(list(headers.values()))

        for order in self:
            for line in order.order_line:
                row = {}
                row["hinh_thuc_ban_hang"] = "Bán hàng hóa trong nước"

                payment_terms = self.get_phuong_thuc_thanh_toan(order)
                row["phuong_thuc_thanh_toan"] = payment_terms

                row["kiem_phieu_xuat_kho"] = "Có"
                row["lap_kem_hoa_don"] = "Không"

                invoices = order.invoice_ids.filtered(lambda inv: inv.state != "cancel")
                row["da_lap_hoa_don"] = "Đã lập" if invoices else "Chưa lập"

                row["ngay_hach_toan"] = (
                    order.create_date.strftime("%d/%m/%Y") if order.create_date else ""
                )
                row["ngay_chung_tu"] = (
                    order.create_date.strftime("%d/%m/%Y") if order.create_date else ""
                )
                row["so_chung_tu"] = invoices[0].name if invoices else ""
                row["so_phieu_xuat"] = self.get_so_phieu_xuat(order)
                row["mau_so_hd"] = ""
                row["ky_hieu_hd"] = ""
                row["so_hoa_don"] = ""
                row["ngay_hoa_don"] = ""
                row["ma_khach_hang"] = (
                    order.partner_id.ref if order.partner_id.ref else ""
                )
                row["ten_khach_hang"] = (
                    order.partner_id.name if order.partner_id else ""
                )
                row["dia_chi"] = (
                    order.partner_id.contact_address if order.partner_id else ""
                )
                row["ma_so_thue"] = order.partner_id.vat if order.partner_id.vat else ""
                row["don_vi_giao_dai_ly"] = ""
                row["nguoi_nop"] = ""
                row["nop_vao_tk"] = ""
                row["ten_ngan_hang"] = ""
                row["dien_giai_ly_do_nop"] = ""
                row["ly_do_xuat"] = "Xuất kho bán hàng"

                salesperson_properties = self.get_salesperson_employee_properties(order)
                row["ma_nhan_vien_ban_hang"] = (
                    salesperson_properties.get("employee_id", "")
                    if salesperson_properties
                    else ""
                )

                row["so_chung_tu_kem_theo_phieu_thu"] = ""
                row["so_chung_tu_kem_theo_phieu_xuat"] = 1

                if payment_terms in [
                    self.PAYMENT_TERMS_IMMEDIATE_CASH,
                    self.PAYMENT_TERMS_IMMEDIATE_TRANSFER,
                ]:
                    due_date = order.create_date
                else:
                    # Add 7 days to the creation date
                    due_date = order.create_date + timedelta(days=7)
                row["han_thanh_toan"] = due_date.strftime("%d/%m/%Y")

                row["loai_tien"] = "VND"
                row["ty_gia"] = 1

                if not line.product_id:
                    row["la_dong_ghi_chu"] = "Có"
                else:
                    row["ma_hang"] = (
                        line.product_id.default_code if line.product_id else ""
                    )
                    row["thuoc_combo"] = ""
                    row["ten_hang"] = line.product_id.name
                    row["hang_khuyen_mai"] = "Không"
                    row["tk_tien_chi_phi_no"] = "1311"
                    row["tk_doanh_thu_co"] = "5111"
                    row["dvt"] = line.product_uom.name if line.product_uom else ""
                    row["so_luong"] = line.product_uom_qty
                    row["don_gia"] = line.price_unit
                    row["thanh_tien"] = row["so_luong"] * row["don_gia"]
                    row["thanh_tien_quy_doi"] = row["thanh_tien"] * row["ty_gia"]
                    row["ty_le_ck"] = ""
                    row["tien_chiet_khau"] = (
                        row["thanh_tien"] * float(row["ty_le_ck"]) / 100
                        if row["ty_le_ck"]
                        else 0
                    )
                    row["tien_chiet_khau_quy_doi"] = (
                        row["tien_chiet_khau"] * row["ty_gia"]
                    )
                    row["tk_chiet_khau"] = "5111"
                    row["gia_tinh_thue_xk"] = ""
                    row["phan_tram_thue_xuat_khau"] = ""
                    row["tien_thue_xuat_khau"] = ""
                    row["tk_thue_xuat_khau"] = ""

                    tax = line.tax_id[0] if line.tax_id else None
                    row["phan_tram_thue_gtgt"] = int(tax.amount) if tax else ""

                    row["phan_tram_thue_suat_khac"] = ""

                    row["tien_thue_gtgt"] = (
                        (row["thanh_tien"] - row["tien_chiet_khau"])
                        * float(row["phan_tram_thue_gtgt"])
                        / 100
                    )

                    row["tien_thue_gtgt_quy_doi"] = (
                        row["tien_thue_gtgt"] * row["ty_gia"]
                    )
                    row["tk_thue_gtgt"] = "33311"
                    row["hh_khong_th_tren_to_khai_thue_gtgt"] = ""
                    row["ma_khoan_muc_chi_phi"] = ""
                    row["ma_don_vi"] = ""
                    row["ma_doi_tuong_thcp"] = ""
                    row["ma_cong_trinh"] = ""
                    row["so_don_dat_hang"] = ""
                    row["so_hop_dong_ban"] = ""
                    row["ma_thong_ke"] = ""
                    row["so_khe_uoc_cho_vay"] = ""
                    row["cp_khong_hop_ly"] = ""
                    row["ma_kho"] = "001"
                    row["tk_gia_von"] = "632"
                    row["tk_kho"] = "152"

                row_values = [row.get(key, "") for key in headers.keys()]
                ws.append(row_values)

        file_stream = io.BytesIO()
        wb.save(file_stream)
        file_stream.seek(0)

        return file_stream.read()

    def export_custom_excel(self):
        base_url = request.env["ir.config_parameter"].sudo().get_param("web.base.url")
        order_ids = ",".join(str(id) for id in self.ids)
        url = f"{base_url}/adt_sale_order_export/export_excel?order_ids={order_ids}"

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new",
        }

    def get_phuong_thuc_thanh_toan(self, order):
        """
        This method checks the payment term for the order.
        If it's not 'Thu tiền ngay - Tiền mặt' or 'Thu tiền ngay - Chuyển khoản',
        it returns 'Chưa thu tiền'.
        """
        if order.payment_term_id:
            payment_terms = order.payment_term_id.with_context(lang="vi_VN").name
            if payment_terms not in [
                self.PAYMENT_TERMS_IMMEDIATE_CASH,
                self.PAYMENT_TERMS_IMMEDIATE_TRANSFER,
            ]:
                return "Chưa thu tiền"
            else:
                return payment_terms

        return "Chưa thu tiền"

    def get_so_phieu_xuat(self, order):
        """
        This method returns the 'Mã của đơn giao hàng đầu tiên' (delivery order reference)
        for the first non-cancelled delivery order with prefix 'WH/PICK/'.
        """
        picking = order.picking_ids.filtered(
            lambda p: p.state != "cancel" and p.name.startswith("WH/PICK/")
        )

        if picking:
            picking_name = picking[0].name
            # Extract numeric part after 'WH/PICK/'
            return picking_name.split("WH/PICK/")[1]

        return ""

    def get_salesperson_employee_properties(self, order):
        """
        This method returns the employee properties of the salesperson (user) associated with the sale order.
        """
        salesperson = order.user_id
        employee = (
            salesperson.employee_id
            if hasattr(salesperson, "employee_id") and salesperson.employee_id
            else None
        )

        if employee:
            return {
                "name": employee.name,
                "job_title": employee.job_title,
                "department": (
                    employee.department_id.name if employee.department_id else ""
                ),
                "work_phone": employee.work_phone,
                "work_email": employee.work_email,
                "employee_id": (
                    list(employee.employee_properties.values())[0]
                    if employee.employee_properties
                    else ""
                ),
            }
        return {}
