import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class SimplePDFExporter:
    """Simplified PDF exporter for testing"""
    
    def __init__(self, db, models):
        self.db = db
        self.models = models
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'exports')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def export_simple_pdf(self):
        """Export a simple PDF without complex tables"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'simple_migration_plan_{timestamp}.pdf'
            filepath = os.path.join(self.output_dir, filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            story.append(Paragraph("Cloud Migration Plan", styles['Title']))
            story.append(Spacer(1, 20))
            
            # Executive Summary
            story.append(Paragraph("Executive Summary", styles['Heading1']))
            
            # Get basic counts
            summary_data = self._get_basic_summary()
            story.append(Paragraph(f"Total Servers: {summary_data['servers_count']}", styles['Normal']))
            story.append(Paragraph(f"Total Databases: {summary_data['databases_count']}", styles['Normal']))
            story.append(Paragraph(f"Total File Shares: {summary_data['file_shares_count']}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Cost Information
            story.append(Paragraph("Cost Analysis", styles['Heading1']))
            story.append(Paragraph("Annual Cloud Cost: $50,000", styles['Normal']))
            story.append(Paragraph("Migration Services Cost: $75,000", styles['Normal']))
            story.append(Paragraph("Total First Year Cost: $125,000", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Timeline
            story.append(Paragraph("Migration Timeline", styles['Heading1']))
            story.append(Paragraph("Total Duration: 24 weeks", styles['Normal']))
            story.append(Paragraph("Key Milestones: 5 major milestones", styles['Normal']))
            
            # Build PDF
            doc.build(story)
            return filepath
            
        except Exception as e:
            raise Exception(f"Failed to export simple PDF: {str(e)}")
    
    def _get_basic_summary(self):
        """Get basic summary without complex queries"""
        try:
            Server = self.models.get('Server')
            Database = self.models.get('Database') 
            FileShare = self.models.get('FileShare')
            
            servers_count = 0
            databases_count = 0
            file_shares_count = 0
            
            if Server:
                servers_count = Server.query.count()
            if Database:
                databases_count = Database.query.count()
            if FileShare:
                file_shares_count = FileShare.query.count()
                
            return {
                'servers_count': servers_count,
                'databases_count': databases_count, 
                'file_shares_count': file_shares_count
            }
        except Exception as e:
            # Return fallback data if queries fail
            return {
                'servers_count': 0,
                'databases_count': 0,
                'file_shares_count': 0
            }
