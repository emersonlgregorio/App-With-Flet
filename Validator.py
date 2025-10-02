import locale

class Validator():

    def format_to_int(value):
        try:
            return int(value)
        except Exception:
            return None

    def format_to_float(value):
        value = value.replace(".", "")
        value = value.replace(",", ".")
        try:
            return(float(value))
        except Exception:
            return None

    def format_to_currency(value):
        # Configurar locale de forma segura
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
        except locale.Error:
            try:
                locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            except locale.Error:
                try:
                    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
                except locale.Error:
                    # Usar locale padrão se pt_BR não estiver disponível
                    pass
        
        try:
            return locale.currency(value, symbol=False, grouping=True)
        except Exception:
            # Fallback para formatação manual se locale falhar
            return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")