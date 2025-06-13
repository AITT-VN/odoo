from odoo import models
import io
from openpyxl import Workbook
from odoo.http import request


class ExpenseExport(models.Model):
    _inherit = "hr.expense"

    def generate_export_expenses(self):

        wb = Workbook()
        ws = wb.active
        ws.title = "Expenses"

        headers = {
            "trang_thai": "Trạng thái",
            "phuong_thuc_thanh_toan": "Phương thức thanh toán",
            "nhan_kem_hoa_doen": "Nhận kèm hóa đơn",
            "la_cp_mua_hang": "Là CP mua hàng",
            "ngay_hach_toan": "Ngày hạch toán (*)",
            "ngay_chung_tu": "Ngày chứng từ (*)",
            "so_chung_tu": "Số chứng từ (*)",
            "so_tai_khoan_chi": "Số tài khoản chi",
            "ten_ngan_hang_chi": "Tên ngân hàng chi",
            "nha_cung_cap": "Nhà cung cấp",
            "dia_chi": "Địa chỉ",
            "dien_giai_ly_do_chi_noi_dung_thanh_toan": "Diễn giải/Lý do chi/Nội dung thanh toán",
            "so_tai_khoan_nhan": "Số tài khoản nhận",
            "ten_ngan_hang_nhan": "Tên ngân hàng nhận",
            "ma_nhan_vien_mua_hang": "Mã nhân viên mua hàng",
            "han_thanh_toan": "Hạn thanh toán",
            "loai_tien": "Loại tiền",
            "ty_gia": "Tỷ giá",
            "ma_dich_vu": "Mã dịch vụ (*)",
            "ten_dich_vu": "Tên dịch vụ",
            "la_dong_ghi_chu": "Là dòng ghi chú",
            "tk_kho_tk_chi_phi": "TK kho/TK chi phí (*)",
            "tk_cong_no_tk_tien": "TK công nợ/TK tiền (*)",
            "ma_doi_tuong": "Mã đối tượng",
            "dv_tinh": "ĐVT",
            "so_luong": "Số lượng",
            "don_gia": "Đơn giá",
            "thanh_tien": "Thành tiền",
            "thanh_tien_quy_doi": "Thành tiền quy đổi",
            "ty_le_ck": "Tỷ lệ CK (%)",
            "tien_chiet_khau": "Tiền chiết khấu",
            "tien_chiet_khau_quy_doi": "Tiền chiết khấu quy đổi",
            "ma_khoan_muc_chi_phi": "Mã khoản mục chi phí",
            "ma_don_vi": "Mã đơn vị",
            "ma_doi_tuong_thcp": "Mã đối tượng THCP",
            "ma_cong_trinh": "Mã công trình",
            "so_don_dat_hang": "Số đơn đặt hàng",
            "so_hop_dong_mua": "Số hợp đồng mua",
            "so_hop_dong_ban": "Số hợp đồng bán",
            "ma_thong_ke": "Mã thống kê",
            "so_khe_uoc_di_vay": "Số khế ước đi vay",
            "so_khe_uoc_cho_vay": "Số khế ước cho vay",
            "cp_khong_hop_ly": "CP không hợp lý",
            "phan_tram_thue_gtgt": "% thuế GTGT",
            "phan_tram_thue_suat_khac": "% thuế suất KHAC",
            "tien_thue_gtgt": "Tiền thuế GTGT",
            "tien_thue_gtgt_quy_doi": "Tiền thuế GTGT quy đổi",
            "tk_thue_gtgt": "TK thuế GTGT",
            "ngay_hoa_don": "Ngày hóa đơn",
            "so_hoa_don": "Số hóa đơn",
            "mau_so_hd": "Mẫu số HĐ",
            "ky_hieu_hd": "Ký hiệu HĐ",
            "nhom_hhdv_mua_vao": "Nhóm HHDV mua vào",
            "ma_ncc": "Mã NCC",
            "ten_ncc": "Tên NCC",
            "ma_so_thue_ncc": "Mã số thuế NCC",
            "dia_chi_ncc": "Địa chỉ NCC",
        }

        ws.append(list(headers.values()))

        state_labels = {
            "draft": "Chờ báo cáo",
            "reported": "Để Trình",
            "submitted": "Để Trình",
            "approved": "Đã Phê Duyệt",
            "done": "Hoàn tất",
            "refused": "Bị từ chối",
        }

        for expense in self:
            row = {}
            row["trang_thai"] = state_labels.get(expense.state)
            row["phuong_thuc_thanh_toan"] = ""
            row["nhan_kem_hoa_doen"] = ""
            row["la_cp_mua_hang"] = ""
            row["ngay_hach_toan"] = (
                expense.accounting_date.strftime("%d/%m/%Y")
                if expense.accounting_date
                else ""
            )
            row["ngay_chung_tu"] = ""
            row["so_chung_tu"] = ""
            row["so_tai_khoan_chi"] = ""
            row["ten_ngan_hang_chi"] = ""
            row["nha_cung_cap"] = expense.vendor_id.name or ""
            row["dia_chi"] = expense.vendor_id.contact_address or ""
            row["dien_giai_ly_do_chi_noi_dung_thanh_toan"] = expense.name
            row["so_tai_khoan_nhan"] = ""
            row["ten_ngan_hang_nhan"] = ""
            row["ma_nhan_vien_mua_hang"] = (
                next(iter(expense.employee_id.employee_properties.values())) or ""
                if expense.employee_id.employee_properties
                else ""
            )
            row["han_thanh_toan"] = ""
            row["loai_tien"] = "VND"
            row["ty_gia"] = 1
            row["ma_dich_vu"] = expense.product_id.default_code or ""
            row["ten_dich_vu"] = expense.product_id.name
            row["la_dong_ghi_chu"] = ""
            row["tk_kho_tk_chi_phi"] = "1561"
            row["tk_cong_no_tk_tien"] = "331"
            row["ma_doi_tuong"] = expense.vendor_id.ref or ""
            row["dv_tinh"] = ""
            row["so_luong"] = expense.quantity
            row["don_gia"] = expense.price_unit
            row["thanh_tien"] = row["so_luong"] * row["don_gia"]
            row["thanh_tien_quy_doi"] = row["thanh_tien"] * row["ty_gia"]
            row["ty_le_ck"] = 0
            row["tien_chiet_khau"] = row["thanh_tien"] * row["ty_le_ck"] / 100
            row["tien_chiet_khau_quy_doi"] = row["tien_chiet_khau"] * row["don_gia"]
            row["ma_khoan_muc_chi_phi"] = ""
            row["ma_don_vi"] = ""
            row["ma_doi_tuong_thcp"] = ""
            row["ma_cong_trinh"] = ""
            row["so_don_dat_hang"] = ""
            row["so_hop_dong_mua"] = ""
            row["so_hop_dong_ban"] = ""
            row["ma_thong_ke"] = ""
            row["so_khe_uoc_di_vay"] = ""
            row["so_khe_uoc_cho_vay"] = ""
            row["cp_khong_hop_ly"] = "Không"
            row["phan_tram_thue_gtgt"] = (
                expense.tax_ids[0].amount if expense.tax_ids else 0
            )
            row["phan_tram_thue_suat_khac"] = ""
            row["tien_thue_gtgt"] = (
                (row["thanh_tien"] - row["tien_chiet_khau"])
                * row["phan_tram_thue_gtgt"]
                / 100
            )
            row["tien_thue_gtgt_quy_doi"] = (
                (row["tien_thue_gtgt"] * row["ty_gia"]) * 10 / 100
            )
            row["tk_thue_gtgt"] = "1331"
            row["ngay_hoa_don"] = ""
            row["so_hoa_don"] = ""
            row["mau_so_hd"] = ""
            row["ky_hieu_hd"] = ""
            row["nhom_hhdv_mua_vao"] = ""
            row["ma_ncc"] = expense.vendor_id.ref or ""
            row["ten_ncc"] = expense.vendor_id.name or ""
            row["ma_so_thue_ncc"] = expense.vendor_id.vat or ""
            row["dia_chi_ncc"] = expense.vendor_id.contact_address or ""

            row_values = [row.get(key, "") for key in headers.keys()]
            ws.append(row_values)

        file_stream = io.BytesIO()
        wb.save(file_stream)
        file_stream.seek(0)

        return file_stream.read()

    def export_selected_expenses(self, expense_ids):
        base_url = request.env["ir.config_parameter"].sudo().get_param("web.base.url")
        expense_ids = ",".join(str(id) for id in expense_ids)
        url = f"{base_url}/adt_expenses_export/export_expense?expense_ids={expense_ids}"

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new",
        }
