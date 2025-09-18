#!/usr/bin/env python3
"""
PDF Report Generator for KrishiVaani Smart Crop Based Analysis
Creates comprehensive reports with crop analysis, soil requirements, and location data
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white, darkgreen, darkblue
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from datetime import datetime
import io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

class CropReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for the PDF report"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=darkgreen
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            textColor=darkblue,
            borderWidth=1,
            borderColor=darkblue,
            borderPadding=5
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=16,
            textColor=darkgreen,
            leftIndent=0
        ))
        
        # Info box style
        self.styles.add(ParagraphStyle(
            name='InfoBox',
            parent=self.styles['Normal'],
            fontSize=10,
            backgroundColor=HexColor('#f8f9fa'),
            borderWidth=1,
            borderColor=HexColor('#dee2e6'),
            borderPadding=8,
            spaceAfter=12
        ))
    
    def create_header(self, story):
        """Create report header with title and metadata"""
        # Title
        title = Paragraph("🌱 Smart Crop Selection System", self.styles['CustomTitle'])
        story.append(title)
        
        # Subtitle
        subtitle = Paragraph("Comprehensive Soil Analysis & Location Report", self.styles['CustomSubtitle'])
        story.append(subtitle)
        
        # Metadata
        current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        metadata = f"<b>Report Generated:</b> {current_time}<br/><b>System:</b> AI-Powered Agricultural Analysis"
        meta_para = Paragraph(metadata, self.styles['InfoBox'])
        story.append(meta_para)
        story.append(Spacer(1, 20))
    
    def create_crop_analysis_section(self, story, crop_data):
        """Create crop analysis section"""
        # Section header
        header = Paragraph("📊 Crop Analysis Summary", self.styles['SectionHeader'])
        story.append(header)
        
        # Basic crop info table
        crop_info_data = [
            ['Crop Name', crop_data['crop']],
            ['Growing Season', crop_data['growing_season']],
            ['Growth Duration', crop_data['growth_duration']],
            ['Recommended Soil Types', ', '.join(crop_data['recommended_soil_types'])]
        ]
        
        crop_info_table = Table(crop_info_data, colWidths=[2*inch, 4*inch])
        crop_info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#e8f5e8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(crop_info_table)
        story.append(Spacer(1, 20))
    
    def create_soil_requirements_section(self, story, soil_requirements):
        """Create soil requirements section"""
        header = Paragraph("🌱 Optimal Soil Requirements", self.styles['SectionHeader'])
        story.append(header)
        
        # Soil parameters table
        soil_data = [['Parameter', 'Optimal Range', 'Unit', 'Description']]
        
        for param, details in soil_requirements.items():
            param_name = self.get_parameter_display_name(param)
            optimal_range = f"{details['optimal'][0]} - {details['optimal'][1]}"
            unit = details['unit']
            description = details['description']
            
            soil_data.append([param_name, optimal_range, unit, description])
        
        soil_table = Table(soil_data, colWidths=[1.2*inch, 1*inch, 0.8*inch, 3*inch])
        soil_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f8f9fa')])
        ]))
        
        story.append(soil_table)
        story.append(Spacer(1, 20))
    
    def create_fertilizer_section(self, story, fertilizer_data, fertilizer_schedule):
        """Create fertilizer recommendations section"""
        header = Paragraph("💡 Fertilizer Recommendations", self.styles['SectionHeader'])
        story.append(header)
        
        # Fertilizer table
        fert_data = [['Fertilizer', 'Composition', 'Application Rate', 'Benefits']]
        
        for fert in fertilizer_data:
            name = fert['name']
            composition = fert['details']['composition']
            app_rate = fert['details']['application_rate']
            benefits = fert['details']['benefits']
            
            fert_data.append([name, composition, app_rate, benefits])
        
        fert_table = Table(fert_data, colWidths=[1.2*inch, 1.5*inch, 1.3*inch, 2*inch])
        fert_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f8f9fa')])
        ]))
        
        story.append(fert_table)
        story.append(Spacer(1, 12))
        
        # Application schedule
        schedule_text = f"<b>Application Schedule:</b><br/>{fertilizer_schedule}"
        schedule_para = Paragraph(schedule_text, self.styles['InfoBox'])
        story.append(schedule_para)
        story.append(Spacer(1, 20))
    
    def create_location_section(self, story, location_data, crop_name):
        """Create Indian locations section"""
        if not location_data or 'message' in location_data:
            return
        
        header = Paragraph("🇮🇳 Best Growing Locations in India", self.styles['SectionHeader'])
        story.append(header)
        
        # Major states
        states_text = "<b>Major Growing States:</b><br/>" + ", ".join(location_data['major_states'])
        states_para = Paragraph(states_text, self.styles['Normal'])
        story.append(states_para)
        story.append(Spacer(1, 8))
        
        # Top districts
        districts_text = "<b>Top Districts:</b><br/>" + "<br/>".join([f"• {district}" for district in location_data['top_districts']])
        districts_para = Paragraph(districts_text, self.styles['Normal'])
        story.append(districts_para)
        story.append(Spacer(1, 8))
        
        # Production share
        production_text = f"<b>Production Share:</b><br/>{location_data['production_share']}"
        production_para = Paragraph(production_text, self.styles['InfoBox'])
        story.append(production_para)
        
        # Agro-climatic zones
        zones_text = "<b>Suitable Agro-Climatic Zones:</b><br/>" + ", ".join(location_data['agro_climatic_zones'])
        zones_para = Paragraph(zones_text, self.styles['Normal'])
        story.append(zones_para)
        story.append(Spacer(1, 12))
        
        # Best regions (if available)
        if 'best_regions' in location_data:
            best_regions_text = "<b>Regional Specializations:</b><br/>"
            for category, regions in location_data['best_regions'].items():
                category_name = category.replace('_', ' ').title()
                if isinstance(regions, list):
                    regions_str = ", ".join(regions)
                else:
                    regions_str = str(regions)
                best_regions_text += f"<b>{category_name}:</b> {regions_str}<br/>"
            
            best_regions_para = Paragraph(best_regions_text, self.styles['InfoBox'])
            story.append(best_regions_para)
        
        story.append(Spacer(1, 20))
    
    def create_ai_prediction_section(self, story, prediction_data):
        """Create AI prediction results section"""
        header = Paragraph("🤖 AI Crop Predictions", self.styles['SectionHeader'])
        story.append(header)
        
        # Input parameters
        input_text = "<b>Soil Parameters Analyzed:</b><br/>"
        for param, value in prediction_data['input_parameters'].items():
            param_name = self.get_parameter_display_name(param)
            unit = self.get_parameter_unit(param)
            input_text += f"<b>{param_name}:</b> {value} {unit}<br/>"
        
        input_para = Paragraph(input_text, self.styles['InfoBox'])
        story.append(input_para)
        story.append(Spacer(1, 12))
        
        # Recommendations table
        rec_data = [['Rank', 'Crop', 'Confidence', 'Suitability']]
        
        for i, rec in enumerate(prediction_data['recommendations'][:5], 1):
            rank = str(i)
            crop = rec['crop']
            confidence = rec['confidence']
            suitability = "Excellent" if rec['probability'] > 0.7 else "Good" if rec['probability'] > 0.4 else "Fair"
            
            rec_data.append([rank, crop, confidence, suitability])
        
        rec_table = Table(rec_data, colWidths=[0.8*inch, 2*inch, 1.2*inch, 2*inch])
        rec_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#28a745')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f8f9fa')])
        ]))
        
        story.append(rec_table)
        story.append(Spacer(1, 20))
    
    def get_parameter_display_name(self, param):
        """Get display name for parameters"""
        names = {
            'N': 'Nitrogen (N)',
            'P': 'Phosphorus (P)', 
            'K': 'Potassium (K)',
            'ph': 'pH Level',
            'temperature': 'Temperature',
            'humidity': 'Humidity',
            'rainfall': 'Rainfall'
        }
        return names.get(param, param)
    
    def get_parameter_unit(self, param):
        """Get unit for parameters"""
        units = {
            'N': 'mg/kg',
            'P': 'mg/kg',
            'K': 'mg/kg', 
            'ph': '',
            'temperature': '°C',
            'humidity': '%',
            'rainfall': 'mm'
        }
        return units.get(param, '')
    
    def create_footer(self, story):
        """Create report footer"""
        footer_text = """
        <b>Disclaimer:</b> This report is generated by an AI-powered system for informational purposes. 
        Please consult with local agricultural experts and conduct soil tests before making farming decisions.
        The recommendations are based on general agricultural practices and may need adjustment based on 
        local conditions, climate variations, and specific field requirements.
        <br/><br/>
        <b>Generated by:</b> Smart Crop Selection System | <b>Technology:</b> Machine Learning & Agricultural Science
        """
        footer_para = Paragraph(footer_text, self.styles['InfoBox'])
        story.append(Spacer(1, 30))
        story.append(footer_para)
    
    def generate_crop_report(self, crop_data):
        """Generate PDF report for crop analysis"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, 
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Create report sections
        self.create_header(story)
        self.create_crop_analysis_section(story, crop_data)
        self.create_soil_requirements_section(story, crop_data['soil_requirements'])
        self.create_fertilizer_section(story, crop_data['fertilizer_recommendations'], 
                                     crop_data['fertilizer_schedule'])
        self.create_location_section(story, crop_data.get('indian_locations', {}), 
                                   crop_data['crop'])
        self.create_footer(story)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def generate_ai_prediction_report(self, prediction_data):
        """Generate PDF report for AI predictions"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Create report sections
        self.create_header(story)
        self.create_ai_prediction_section(story, prediction_data)
        
        # Add details for best crop recommendation
        if prediction_data['recommendations']:
            best_crop = prediction_data['recommendations'][0]
            if best_crop.get('details'):
                story.append(Spacer(1, 20))
                header = Paragraph(f"📋 Detailed Analysis: {best_crop['crop']}", self.styles['SectionHeader'])
                story.append(header)
                
                # Create mock crop data for detailed analysis
                crop_data = {
                    'crop': best_crop['crop'],
                    'growing_season': best_crop['details']['growing_season'],
                    'growth_duration': best_crop['details']['growth_duration'],
                    'soil_requirements': best_crop['details']['soil_requirements'],
                    'recommended_soil_types': ['Based on AI Analysis']
                }
                
                self.create_soil_requirements_section(story, crop_data['soil_requirements'])
        
        self.create_footer(story)
        
        # Build PDF  
        doc.build(story)
        buffer.seek(0)
        return buffer