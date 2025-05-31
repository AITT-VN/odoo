from odoo import models, fields
import io
from openpyxl import Workbook
from datetime import datetime
from odoo.http import request


class SaleOrder(models.Model):
    _inherit = "sale.order"

    x_custom_field = fields.Char(string="Custom Field")

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
                row["phuong_thuc_thanh_toan"] = "X"
                row["kiem_phieu_xuat_kho"] = "Có"
                row["lap_kem_hoa_don"] = "Không"
                row["da_lap_hoa_don"] = "X"
                row["ngay_hach_toan"] = "X"
                row["ngay_chung_tu"] = "X"
                row["so_chung_tu"] = "X"
                row["so_phieu_xuat"] = "X"
                row["mau_so_hd"] = ""
                row["ky_hieu_hd"] = ""
                row["so_hoa_don"] = ""
                row["ngay_hoa_don"] = ""
                row["ma_khach_hang"] = "X"
                row["ten_khach_hang"] = "X"
                row["dia_chi"] = "X"
                row["ma_so_thue"] = "X"
                row["don_vi_giao_dai_ly"] = ""
                row["nguoi_nop"] = ""
                row["nop_vao_tk"] = ""
                row["ten_ngan_hang"] = ""
                row["dien_giai_ly_do_nop"] = ""
                row["ly_do_xuat"] = "Xuất kho bán hàng"
                row["ma_nhan_vien_ban_hang"] = "X"
                row["so_chung_tu_kem_theo_phieu_thu"] = ""
                row["so_chung_tu_kem_theo_phieu_xuat"] = 1
                row["han_thanh_toan"] = "X"
                row["loai_tien"] = "VND"
                row["ty_gia"] = 1
                row["ma_hang"] = "X"
                row["thuoc_combo"] = ""
                row["ten_hang"] = line.product_id.name
                row["la_dong_ghi_chu"] = "X"
                row["hang_khuyen_mai"] = "X"
                row["tk_tien_chi_phi_no"] = "X"
                row["tk_doanh_thu_co"] = "X"
                row["dvt"] = "ĐVT"
                row["so_luong"] = "X"
                row["don_gia"] = "X"
                row["thanh_tien"] = "X" # row["so_luong"] * row["don_gia"]
                row["thanh_tien_quy_doi"] = "X" # row["thanh_tien"] * row["ty_gia"]
                row["ty_le_ck"] = "X"
                row["tien_chiet_khau"] = "X" # row["thanh_tien"] * row["ty_le_ck"] / 100
                row["tien_chiet_khau_quy_doi"] = "X" # row["tien_chiet_khau"] * row["ty_gia"]
                row["tk_chiet_khau"] = "X"
                row["gia_tinh_thue_xk"] = ""
                row["thue_xuat_khau"] = ""
                row["tien_thue_xuat_khau"] = ""
                row["tk_thue_xuat_khau"] = ""
                row["thue_gtgt"] = ""
                row["thue_suat_khac"] = ""
                row["tien_thue_gtgt"] = "X"
                row["tien_thue_gtgt_quy_doi"] = "X" # row["tien_thue_gtgt"] * row["ty_gia"]
                row["tk_thue_gtgt"] = "X"
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
                row["ma_kho"] = "X"
                row["tk_gia_von"] = "X"
                row["tk_kho"] = "X"

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
