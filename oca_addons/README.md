# Module OCA (Odoo Community Association) dùng kèm bản Odoo 18 này

Chép nguyên bản từ nhánh 18.0, không sửa. Cập nhật: chép lại thư mục module từ repo OCA và ghi commit mới ở bảng dưới.

| Module | Repo OCA | Commit |
|---|---|---|
| `account_financial_report` | [OCA/account-financial-reporting](https://github.com/OCA/account-financial-reporting/tree/18.0) | `dbfd1f4` |
| `date_range` | [OCA/server-ux](https://github.com/OCA/server-ux/tree/18.0) | `00754df` |
| `report_xlsx` | [OCA/reporting-engine](https://github.com/OCA/reporting-engine/tree/18.0) | `e35a0fe` |
| `mis_builder` | [OCA/mis-builder](https://github.com/OCA/mis-builder/tree/18.0) | `4f9eef0` |
| `account_usability` | [OCA/account-financial-tools](https://github.com/OCA/account-financial-tools/tree/18.0) | `7442da0` |

Phụ thuộc Python thêm: `openupgradelib` (mis_builder, account_usability). Addons path phải có thư mục này
(`/opt/odoo18/oca_addons` trên server, `/opt/odoo-src/oca_addons` ở bản dev).
