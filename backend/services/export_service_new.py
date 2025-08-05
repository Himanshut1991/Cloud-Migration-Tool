import os
import pandas as pd
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from docx import Document
from docx.shared import Inches

class ExportService:
    """Export migration plans to various formats"""
    
    def __init__(self, db, models=None):
        self.db = db
        self.models = models or {}
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'exports')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def export_to_excel(self):
        """Export migration plan to Excel format"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'migration_plan_{timestamp}.xlsx'
            filepath = os.path.join(self.output_dir, filename)
            
            # Create workbook with multiple sheets
            wb = Workbook()
            wb.remove(wb.active)  # Remove default sheet
            
            # Create summary sheet
            self._create_summary_sheet(wb)
            
            # Create inventory sheets
            self._create_servers_sheet(wb)
            self._create_databases_sheet(wb)
            self._create_file_shares_sheet(wb)
            
            # Create analysis sheets
            self._create_cost_analysis_sheet(wb)
            self._create_timeline_sheet(wb)
            
            wb.save(filepath)
            return filepath
            
        except Exception as e:
            raise Exception(f"Failed to export to Excel: {str(e)}")
    
    def export_to_pdf(self):
        """Export migration plan to PDF format"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'migration_plan_{timestamp}.pdf'
            filepath = os.path.join(self.output_dir, filename)
            
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=20,
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph("Cloud Migration Plan", title_style))
            story.append(Spacer(1, 20))
            
            # Executive Summary
            story.append(Paragraph("Executive Summary", styles['Heading2']))
            summary_data = self._get_summary_data()
            
            story.append(Paragraph(f"Total Servers: {summary_data['servers_count']}", styles['Normal']))
            story.append(Paragraph(f"Total Databases: {summary_data['databases_count']}", styles['Normal']))
            story.append(Paragraph(f"Total File Shares: {summary_data['file_shares_count']}", styles['Normal']))
            story.append(Paragraph(f"Total Data Volume: {summary_data['total_data_gb']:,.0f} GB", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Cost Analysis
            story.append(Paragraph("Cost Analysis", styles['Heading2']))
            cost_data = self._get_cost_summary()
            
            cost_table_data = [
                ['Cost Category', 'Amount (USD)'],
                ['Cloud Infrastructure (Annual)', f"${cost_data.get('annual_cloud_cost', 0):,.2f}"],
                ['Migration Services (One-time)', f"${cost_data.get('migration_services_cost', 0):,.2f}"],
                ['Total First Year Cost', f"${cost_data.get('total_first_year', 0):,.2f}"]
            ]
            
            cost_table = Table(cost_table_data)
            cost_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(cost_table)
            story.append(Spacer(1, 20))
            
            # Timeline
            story.append(Paragraph("Migration Timeline", styles['Heading2']))
            timeline_data = self._get_timeline_summary()
            story.append(Paragraph(f"Total Duration: {timeline_data.get('total_weeks', 0)} weeks", styles['Normal']))
            story.append(Paragraph(f"Estimated Completion: {timeline_data.get('end_date', 'TBD')}", styles['Normal']))
            
            doc.build(story)
            return filepath
            
        except Exception as e:
            raise Exception(f"Failed to export to PDF: {str(e)}")
    
    def export_to_word(self):
        """Export migration plan to Word document"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'migration_plan_{timestamp}.docx'
            filepath = os.path.join(self.output_dir, filename)
            
            doc = Document()
            
            # Title
            title = doc.add_heading('Cloud Migration Plan', 0)
            title.alignment = 1
            
            # Executive Summary
            doc.add_heading('Executive Summary', level=1)
            summary_data = self._get_summary_data()
            
            summary_para = doc.add_paragraph()
            summary_para.add_run(f"This migration plan covers the migration of {summary_data['servers_count']} servers, ")
            summary_para.add_run(f"{summary_data['databases_count']} databases, and {summary_data['file_shares_count']} file shares ")
            summary_para.add_run(f"to the cloud. The total data volume to be migrated is {summary_data.get('total_data_gb', 0):,.0f} GB.")
            
            # Cost Analysis
            doc.add_heading('Cost Analysis', level=1)
            cost_data = self._get_cost_summary()
            
            cost_table = doc.add_table(rows=4, cols=2)
            cost_table.style = 'Table Grid'
            
            # Headers
            hdr_cells = cost_table.rows[0].cells
            hdr_cells[0].text = 'Cost Category'
            hdr_cells[1].text = 'Amount (USD)'
            
            # Data rows
            cost_table.rows[1].cells[0].text = 'Cloud Infrastructure (Annual)'
            cost_table.rows[1].cells[1].text = f"${cost_data.get('annual_cloud_cost', 0):,.2f}"
            
            cost_table.rows[2].cells[0].text = 'Migration Services (One-time)'
            cost_table.rows[2].cells[1].text = f"${cost_data.get('migration_services_cost', 0):,.2f}"
            
            cost_table.rows[3].cells[0].text = 'Total First Year Cost'
            cost_table.rows[3].cells[1].text = f"${cost_data.get('total_first_year', 0):,.2f}"
            
            # Timeline
            doc.add_heading('Migration Timeline', level=1)
            timeline_data = self._get_timeline_summary()
            doc.add_paragraph(f"Total Duration: {timeline_data.get('total_weeks', 0)} weeks")
            doc.add_paragraph(f"Estimated Completion: {timeline_data.get('end_date', 'TBD')}")
            
            # Inventory Summary
            doc.add_heading('Inventory Summary', level=1)
            inventory_table = doc.add_table(rows=4, cols=2)
            inventory_table.style = 'Table Grid'
            
            inv_rows = [
                ['Servers', str(summary_data['servers_count'])],
                ['Databases', str(summary_data['databases_count'])],
                ['File Shares', str(summary_data['file_shares_count'])],
                ['Total Data (GB)', f"{summary_data['total_data_gb']:,.0f}"]
            ]
            
            for i, (category, count) in enumerate(inv_rows):
                inventory_table.rows[i].cells[0].text = category
                inventory_table.rows[i].cells[1].text = count
            
            doc.save(filepath)
            return filepath
            
        except Exception as e:
            raise Exception(f"Failed to export to Word: {str(e)}")
    
    # Helper methods
    def _create_summary_sheet(self, wb):
        """Create summary sheet in Excel"""
        ws = wb.create_sheet("Summary")
        
        # Header styling
        header_font = Font(bold=True, size=14)
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        # Title
        ws['A1'] = "Cloud Migration Plan Summary"
        ws['A1'].font = Font(bold=True, size=16)
        ws.merge_cells('A1:B1')
        
        # Summary data
        summary_data = self._get_summary_data()
        
        ws['A3'] = "Inventory Summary"
        ws['A3'].font = header_font
        ws['A3'].fill = header_fill
        
        ws['A4'] = "Servers"
        ws['B4'] = summary_data['servers_count']
        ws['A5'] = "Databases"
        ws['B5'] = summary_data['databases_count']
        ws['A6'] = "File Shares"
        ws['B6'] = summary_data['file_shares_count']
        ws['A7'] = "Total Data (GB)"
        ws['B7'] = summary_data['total_data_gb']
        
        # Cost summary
        cost_data = self._get_cost_summary()
        
        ws['A9'] = "Cost Summary"
        ws['A9'].font = header_font
        ws['A9'].fill = header_fill
        
        ws['A10'] = "Annual Cloud Cost"
        ws['B10'] = cost_data['annual_cloud_cost']
        ws['A11'] = "Migration Services"
        ws['B11'] = cost_data['migration_services_cost']
        ws['A12'] = "Total First Year"
        ws['B12'] = cost_data['total_first_year']
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
    
    def _create_servers_sheet(self, wb):
        """Create servers inventory sheet"""
        ws = wb.create_sheet("Servers")
        
        # Headers
        headers = ['Name', 'Environment', 'OS', 'CPU Cores', 'Memory (GB)', 'Storage (GB)', 'Status']
        for i, header in enumerate(headers, 1):
            ws.cell(row=1, column=i, value=header).font = Font(bold=True)
        
        # Get server data
        Server = self.models.get('Server')
        if Server:
            servers = Server.query.all()
            for i, server in enumerate(servers, 2):
                ws.cell(row=i, column=1, value=server.name)
                ws.cell(row=i, column=2, value=server.environment)
                ws.cell(row=i, column=3, value=server.operating_system)
                ws.cell(row=i, column=4, value=server.cpu_cores)
                ws.cell(row=i, column=5, value=server.memory_gb)
                ws.cell(row=i, column=6, value=server.storage_gb)
                ws.cell(row=i, column=7, value=server.status)
    
    def _create_databases_sheet(self, wb):
        """Create databases inventory sheet"""
        ws = wb.create_sheet("Databases")
        
        headers = ['Name', 'Type', 'Version', 'Size (GB)', 'Environment', 'Status']
        for i, header in enumerate(headers, 1):
            ws.cell(row=1, column=i, value=header).font = Font(bold=True)
        
        Database = self.models.get('Database')
        if Database:
            databases = Database.query.all()
            for i, db in enumerate(databases, 2):
                ws.cell(row=i, column=1, value=db.name)
                ws.cell(row=i, column=2, value=db.database_type)
                ws.cell(row=i, column=3, value=db.version)
                ws.cell(row=i, column=4, value=db.size_gb)
                ws.cell(row=i, column=5, value=db.environment)
                ws.cell(row=i, column=6, value=db.status)
    
    def _create_file_shares_sheet(self, wb):
        """Create file shares inventory sheet"""
        ws = wb.create_sheet("File Shares")
        
        headers = ['Name', 'Share Path', 'Total Size (GB)', 'Share Type', 'Environment', 'Status']
        for i, header in enumerate(headers, 1):
            ws.cell(row=1, column=i, value=header).font = Font(bold=True)
        
        FileShare = self.models.get('FileShare')
        if FileShare:
            file_shares = FileShare.query.all()
            for i, fs in enumerate(file_shares, 2):
                ws.cell(row=i, column=1, value=fs.name)
                ws.cell(row=i, column=2, value=fs.share_path)
                ws.cell(row=i, column=3, value=fs.total_size_gb)
                ws.cell(row=i, column=4, value=fs.share_type)
                ws.cell(row=i, column=5, value=fs.environment)
                ws.cell(row=i, column=6, value=fs.status)
    
    def _create_cost_analysis_sheet(self, wb):
        """Create cost analysis sheet"""
        ws = wb.create_sheet("Cost Analysis")
        
        ws['A1'] = "Cost Analysis Summary"
        ws['A1'].font = Font(bold=True, size=14)
        
        cost_data = self._get_cost_summary()
        
        ws['A3'] = "Cost Category"
        ws['B3'] = "Amount (USD)"
        
        cost_items = [
            ('Annual Cloud Infrastructure', cost_data['annual_cloud_cost']),
            ('Migration Services (One-time)', cost_data['migration_services_cost']),
            ('Training & Support', cost_data.get('training_cost', 5000)),
            ('Total First Year Cost', cost_data['total_first_year'])
        ]
        
        for i, (category, amount) in enumerate(cost_items, 4):
            ws.cell(row=i, column=1, value=category)
            ws.cell(row=i, column=2, value=amount)
    
    def _create_timeline_sheet(self, wb):
        """Create timeline sheet"""
        ws = wb.create_sheet("Timeline")
        
        ws['A1'] = "Migration Timeline"
        ws['A1'].font = Font(bold=True, size=14)
        
        timeline_data = self._get_timeline_summary()
        
        ws['A3'] = "Phase"
        ws['B3'] = "Description"
        ws['C3'] = "Duration (weeks)"
        ws['D3'] = "Start Week"
        ws['E3'] = "End Week"
        
        phases = [
            ('Assessment & Planning', 'Inventory assessment and migration planning', 4, 1, 4),
            ('Environment Setup', 'Cloud infrastructure setup', 3, 5, 7),
            ('Data Migration', 'Database and file share migration', 6, 8, 13),
            ('Server Migration', 'Application and server migration', 3, 14, 16)
        ]
        
        for i, (phase, desc, duration, start, end) in enumerate(phases, 4):
            ws.cell(row=i, column=1, value=phase)
            ws.cell(row=i, column=2, value=desc)
            ws.cell(row=i, column=3, value=duration)
            ws.cell(row=i, column=4, value=start)
            ws.cell(row=i, column=5, value=end)
    
    def _get_summary_data(self):
        """Get summary data for reports"""
        Server = self.models.get('Server')
        Database = self.models.get('Database')
        FileShare = self.models.get('FileShare')
        
        servers_count = Server.query.count() if Server else 0
        databases_count = Database.query.count() if Database else 0
        file_shares_count = FileShare.query.count() if FileShare else 0
        
        total_db_size = 0
        total_fs_size = 0
        
        if Database:
            try:
                total_db_size = self.db.session.query(self.db.func.sum(Database.size_gb)).scalar() or 0
            except:
                total_db_size = 0
                
        if FileShare:
            try:
                total_fs_size = self.db.session.query(self.db.func.sum(FileShare.total_size_gb)).scalar() or 0
            except:
                total_fs_size = 0
        
        return {
            'servers_count': servers_count,
            'databases_count': databases_count,
            'file_shares_count': file_shares_count,
            'total_data_gb': total_db_size + total_fs_size
        }
    
    def _get_cost_summary(self):
        """Get cost summary data"""
        summary_data = self._get_summary_data()
        
        # Basic cost calculations based on inventory
        server_cost = summary_data['servers_count'] * 100 * 12  # $100/month per server
        database_cost = summary_data['databases_count'] * 200 * 12  # $200/month per database
        storage_cost = summary_data['total_data_gb'] * 0.10 * 12  # $0.10/GB per month
        
        annual_cloud_cost = server_cost + database_cost + storage_cost
        migration_services_cost = summary_data['servers_count'] * 500 + summary_data['databases_count'] * 1000
        
        return {
            'annual_cloud_cost': annual_cloud_cost,
            'migration_services_cost': migration_services_cost,
            'total_first_year': annual_cloud_cost + migration_services_cost,
            'training_cost': 5000
        }
    
    def _get_timeline_summary(self):
        """Get timeline summary data"""
        summary_data = self._get_summary_data()
        
        # Calculate timeline based on inventory
        base_weeks = 8
        additional_weeks = (summary_data['servers_count'] // 10) + (summary_data['databases_count'] // 5)
        total_weeks = base_weeks + additional_weeks
        
        return {
            'total_weeks': total_weeks,
            'end_date': 'Based on selected start date',
            'phases': 4,
            'critical_path': ['Assessment', 'Data Migration', 'Server Migration']
        }
