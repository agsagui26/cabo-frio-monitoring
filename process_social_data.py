import json
import re
from collections import defaultdict, Counter
from datetime import datetime
import os

class CaboFrioSocialMonitor:
    def __init__(self):
        self.comments = []
        self.bairros_ruas = self.get_cabo_frio_locations()
        self.temas = {
            'Saneamento': ['esgoto', 'água', 'saneamento', 'fossa', 'bueiro', 'enchente', 'alagamento'],
            'Estradas': ['estrada', 'rua', 'asfalto', 'buraco', 'pavimentação', 'via'],
            'Ordenamento': ['fiscal', 'ordem', 'comércio ambulante', 'irregular', 'ocupação'],
            'Saúde': ['saúde', 'hospital', 'posto', 'upa', 'médico', 'atendimento'],
            'Segurança': ['polícia', 'segurança', 'assalto', 'roubo', 'violência', 'pm'],
            'Iluminação': ['luz', 'iluminação', 'poste', 'escuro', 'lampada'],
            'Lixo': ['lixo', 'coleta', 'sujeira', 'entulho', 'taxa do lixo'],
            'Moradores de rua': ['morador de rua', 'mendigo', 'situação de rua'],
            'Mobilidade': ['ônibus', 'transporte', 'trânsito', 'mobilidade'],
            'Esporte/lazer': ['esporte', 'praça', 'lazer', 'quadra', 'campo'],
            'Educação': ['escola', 'educação', 'creche', 'professor'],
            'Turismo': ['turismo', 'praia', 'turista'],
            'Pediatria': ['criança', 'pediatra', 'infantil'],
            'Canil municipal': ['canil', 'cachorro', 'animal', 'pet']
        }
        
    def get_cabo_frio_locations(self):
        """Principais bairros e localidades de Cabo Frio"""
        return {
            'Centro': ['centro', 'praça porto rocha', 'rua barão do rio branco'],
            'Braga': ['braga', 'jardim caiçara'],
            'Passagem': ['passagem', 'praia do siqueira'],
            'Peró': ['peró', 'praia do peró'],
            'Ogiva': ['ogiva'],
            'Palmeiras': ['palmeiras'],
            'São Cristóvão': ['são cristóvão', 'são cristovão'],
            'Jacaré': ['jacaré'],
            'Tamoios': ['tamoios'],
            'Unamar': ['unamar'],
            'Guarani': ['guarani'],
            'Monte Alto': ['monte alto'],
            'Gamboa': ['gamboa'],
            'Manoel Corrêa': ['manoel corrêa', 'manoel correa'],
            'Jardim Esperança': ['jardim esperança', 'esperança'],
            'Portinho': ['portinho'],
            'Foguete': ['foguete'],
            'Praia do Forte': ['praia do forte', 'forte']
        }
    
    def analyze_sentiment(self, text):
        """Análise de sentimento baseada em palavras-chave"""
        text_lower = text.lower()
        
        # Palavras positivas
        positive_words = ['obrigad', 'parabéns', 'excelente', 'ótimo', 'bom', 'maravilh', 
                         'agrade', 'sucesso', 'apoio', 'top', 'legal', 'show']
        
        # Palavras negativas
        negative_words = ['absurdo', 'vergonha', 'péssim', 'horrível', 'lamentável', 
                         'inadmissível', 'ridícul', 'não', 'nunca', 'nada', 'caro',
                         'aumento', 'abuso', 'roubo', 'ladrão', 'corrupto']
        
        # Ironia/Sarcasmo
        irony_markers = ['né', 'claro', 'com certeza', 'obvio', 'parabéns viu']
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        has_irony = any(marker in text_lower for marker in irony_markers)
        
        # Se tem ironia e palavras positivas, inverte
        if has_irony and pos_count > 0:
            return 'negativo'
        
        if neg_count > pos_count:
            return 'negativo'
        elif pos_count > neg_count:
            return 'positivo'
        else:
            return 'neutro'
    
    def extract_location(self, text):
        """Extrai bairros e ruas mencionados"""
        text_lower = text.lower()
        locations = []
        
        for bairro, keywords in self.bairros_ruas.items():
            for keyword in keywords:
                if keyword in text_lower:
                    locations.append(bairro)
                    break
        
        return locations if locations else ['Não especificado']
    
    def extract_theme(self, text):
        """Extrai temas mencionados"""
        text_lower = text.lower()
        themes = []
        
        for tema, keywords in self.temas.items():
            for keyword in keywords:
                if keyword in text_lower:
                    themes.append(tema)
                    break
        
        return themes if themes else ['Outros']
    
    def check_critical_keywords(self, text):
        """Verifica palavras críticas que sempre devem ser monitoradas"""
        text_lower = text.lower()
        alerts = []
        
        if any(word in text_lower for word in ['milicia', 'miliciano', 'milícia']):
            alerts.append('ALERTA: Menção a milícia')
        
        if any(word in text_lower for word in ['governo do estado', 'governador', 'claudio castro']):
            alerts.append('ALERTA: Menção ao governo estadual')
        
        return alerts
    
    def load_json_file(self, filepath):
        """Carrega arquivo JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else [data]
        except Exception as e:
            print(f"Erro ao carregar {filepath}: {e}")
            return []
    
    def process_comment(self, comment_data, source_file):
        """Processa um comentário individual"""
        text = comment_data.get('text', '')
        
        if not text or len(text.strip()) < 3:
            return None
        
        return {
            'text': text,
            'username': comment_data.get('ownerUsername', 'Anônimo'),
            'timestamp': comment_data.get('timestamp', ''),
            'likes': comment_data.get('likesCount', 0),
            'replies': comment_data.get('repliesCount', 0),
            'sentiment': self.analyze_sentiment(text),
            'locations': self.extract_location(text),
            'themes': self.extract_theme(text),
            'alerts': self.check_critical_keywords(text),
            'source': source_file,
            'url': comment_data.get('commentUrl', '')
        }
    
    def analyze_files(self, file_paths):
        """Analisa todos os arquivos JSON"""
        all_comments = []
        
        for filepath in file_paths:
            filename = os.path.basename(filepath)
            data = self.load_json_file(filepath)
            
            for item in data:
                processed = self.process_comment(item, filename)
                if processed:
                    all_comments.append(processed)
        
        return all_comments
    
    def generate_report(self, comments):
        """Gera relatório consolidado"""
        total = len(comments)
        
        # Contagem de sentimentos
        sentiments = Counter([c['sentiment'] for c in comments])
        
        # Localizações mais mencionadas
        locations = []
        for c in comments:
            locations.extend(c['locations'])
        location_count = Counter(locations)
        
        # Temas mais mencionados
        themes = []
        for c in comments:
            themes.extend(c['themes'])
        theme_count = Counter(themes)
        
        # Alertas críticos
        all_alerts = []
        for c in comments:
            all_alerts.extend(c['alerts'])
        
        # Principais comentários negativos
        negative_comments = [c for c in comments if c['sentiment'] == 'negativo']
        negative_comments.sort(key=lambda x: int(x.get('likes', 0)) + int(x.get('replies', 0)), reverse=True)
        
        report = {
            'total_comments': total,
            'sentiments': dict(sentiments),
            'locations': dict(location_count.most_common(15)),
            'themes': dict(theme_count.most_common()),
            'critical_alerts': all_alerts,
            'top_negative_comments': negative_comments[:20],
            'all_comments': comments
        }
        
        return report

# Processar arquivos
monitor = CaboFrioSocialMonitor()

files = [
    '/mnt/user-data/uploads/IG-JanioMendes.json',
    '/mnt/user-data/uploads/IG-Moniquebispo.json',
    '/mnt/user-data/uploads/fb-Paula_Mendes.json',
    '/mnt/user-data/uploads/fb-drserginho.json',
    '/mnt/user-data/uploads/fb-diversosposts.json',
    '/mnt/user-data/uploads/comments_data.json'
]

comments = monitor.analyze_files(files)
report = monitor.generate_report(comments)

# Salvar relatório
with open('/home/claude/report_data.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"✓ Processados {report['total_comments']} comentários")
print(f"✓ Sentimentos: {report['sentiments']}")
print(f"✓ Relatório salvo em report_data.json")
