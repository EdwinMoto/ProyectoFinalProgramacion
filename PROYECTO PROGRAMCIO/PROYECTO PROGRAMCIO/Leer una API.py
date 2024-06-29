from PyQt5 import QtWidgets, uic
import sys
import requests
import sqlite3

def obtener_conexion():
    return sqlite3.connect('Almacenamiento_API.db')

def creacion_de_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dominio TEXT NOT NULL,
        correo TEXT NOT NULL,
        nombre TEXT,
        posicion TEXT
    )
    ''')
    conexion.commit()
    conexion.close()
    QtWidgets.QMessageBox.information(None, "Información", "Tabla 'emails' creada correctamente.")

def solicitud_api(dominio):
    api_key = 'a0db1cce484acf3201b469d5f942887c6e793741'
    url = f"https://api.hunter.io/v2/domain-search?domain={dominio}&api_key={api_key}"

    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        datos = respuesta.json()
        QtWidgets.QMessageBox.information(None, "Información", "Solicitud a la API de Hunter.io correctamente funcional.")
    except requests.exceptions.RequestException as e:
        QtWidgets.QMessageBox.warning(None, "Error", f"Error al obtener datos de Hunter.io: {e}")
        datos = None

    if datos and 'data' in datos and 'emails' in datos['data']:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        for email in datos['data']['emails']:
            cursor.execute('''
            INSERT INTO emails (dominio, correo, nombre, posicion)
            VALUES (?, ?, ?, ?)
            ''', (dominio, email['value'], email.get('first_name', '') + ' ' + email.get('last_name', ''), email.get('position', '')))
        conexion.commit()
        conexion.close()
        QtWidgets.QMessageBox.information(None, "Información", "Datos de Hunter.io insertados correctamente.")
    else:
        QtWidgets.QMessageBox.warning(None, "Error", "No se encontraron datos de correos electrónicos para el dominio ingresado.")

def encontrar_email(dominio, nombre, apellido):
    api_key = 'a0db1cce484acf3201b469d5f942887c6e793741'
    url = f"https://api.hunter.io/v2/email-finder?domain={dominio}&first_name={nombre}&last_name={apellido}&api_key={api_key}"
    
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        datos = respuesta.json()
        email = datos.get('data', {}).get('email', None)
        if email:
            QtWidgets.QMessageBox.information(None, "Información", f"Correo encontrado: {email}")
            return email
        else:
            QtWidgets.QMessageBox.warning(None, "Error", "No se encontró un correo electrónico para los datos proporcionados.")
            return None
    except requests.exceptions.RequestException as e:
        QtWidgets.QMessageBox.warning(None, "Error", f"Error al obtener datos de Hunter.io: {e}")
        return None

def verificar_email(email):
    api_key = 'a0db1cce484acf3201b469d5f942887c6e793741'
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"
    
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        datos = respuesta.json()
        resultado = datos.get('data', {}).get('result', None)
        if resultado:
            QtWidgets.QMessageBox.information(None, "Información", f"Resultado de verificación: {resultado}")
            return resultado
        else:
            QtWidgets.QMessageBox.warning(None, "Error", "No se pudo verificar el correo electrónico.")
            return None
    except requests.exceptions.RequestException as e:
        QtWidgets.QMessageBox.warning(None, "Error", f"Error al verificar el correo electrónico: {e}")
        return None

def consultar_datos_emails():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM emails')
    emails = cursor.fetchall()
    conexion.close()
    return emails

def actualizar_correo(email_id, nuevo_correo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM emails WHERE id = ?', (email_id,))
    email = cursor.fetchone()
    if email:
        cursor.execute('''
        UPDATE emails
        SET correo = ?
        WHERE id = ?
        ''', (nuevo_correo, email_id))
        conexion.commit()
        QtWidgets.QMessageBox.information(None, "Información", f"Correo del registro con la ID {email_id} actualizado correctamente.")
    else:
        QtWidgets.QMessageBox.warning(None, "Error", f"No se encontró un registro con id={email_id}.")
    conexion.close()

def eliminar_email(email_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM emails WHERE id = ?', (email_id,))
    email = cursor.fetchone()
    if email:
        cursor.execute('DELETE FROM emails WHERE id = ?', (email_id,))
        conexion.commit()
        QtWidgets.QMessageBox.information(None, "Información", f"Registro con la ID {email_id} eliminado correctamente.")
    else:
        QtWidgets.QMessageBox.warning(None, "Error", f"No se encontró un registro con id={email_id}.")
    conexion.close()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('main_window.ui', self)
        
        self.btn_crear.clicked.connect(creacion_de_tablas)
        self.btn_solicitar.clicked.connect(self.abrir_ventana_api)
        self.btn_consultar.clicked.connect(self.mostrar_emails)
        self.btn_modificar.clicked.connect(self.abrir_ventana_modificar)
        self.btn_eliminar.clicked.connect(self.abrir_ventana_eliminar)
        self.btn_salir.clicked.connect(self.close)
        self.btnEncontrar.clicked.connect(self.abrir_ventana_encontrar)
        self.btnVerificar.clicked.connect(self.abrir_ventana_verificar)

    def abrir_ventana_api(self):
        self.ventana_api = VentanaAPI()
        self.ventana_api.show()

    def abrir_ventana_modificar(self):
        self.ventana_modificar = VentanaModificar()
        self.ventana_modificar.show()

    def abrir_ventana_eliminar(self):
        self.ventana_eliminar = VentanaEliminar()
        self.ventana_eliminar.show()

    def abrir_ventana_encontrar(self):
        self.ventana_encontrar = VentanaEncontrar()
        self.ventana_encontrar.show()

    def abrir_ventana_verificar(self):
        self.ventana_verificar = VentanaVerificar()
        self.ventana_verificar.show()

    def mostrar_emails(self):
        emails = consultar_datos_emails()
        self.tableWidget.setRowCount(len(emails))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Dominio', 'Correo', 'Nombre', 'Posición'])
        
        for row, email in enumerate(emails):
            for col, data in enumerate(email):
                self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(data)))

class VentanaAPI(QtWidgets.QMainWindow):
    def __init__(self):
        super(VentanaAPI, self).__init__()
        uic.loadUi('ventana_api.ui', self)
        self.btnSolicitar.clicked.connect(self.solicitar_api)

    def solicitar_api(self):
        dominio = self.txtDominio.text()
        solicitud_api(dominio)
        self.close()

class VentanaModificar(QtWidgets.QMainWindow):
    def __init__(self):
        super(VentanaModificar, self).__init__()
        uic.loadUi('ventana_modificar.ui', self)
        self.btnModificar.clicked.connect(self.modificar_correo)

    def modificar_correo(self):
        email_id = int(self.txtID.text())
        nuevo_correo = self.txtNuevoCorreo.text()
        actualizar_correo(email_id, nuevo_correo)
        self.close()

class VentanaEliminar(QtWidgets.QMainWindow):
    def __init__(self):
        super(VentanaEliminar, self).__init__()
        uic.loadUi('ventana_eliminar.ui', self)
        self.btnEliminar.clicked.connect(self.eliminar_email)

    def eliminar_email(self):
        email_id = int(self.txtID.text())
        eliminar_email(email_id)
        self.close()

class VentanaEncontrar(QtWidgets.QMainWindow):
    def __init__(self):
        super(VentanaEncontrar, self).__init__()
        uic.loadUi('ventana_encontrar.ui', self)
        self.btnEncontrar.clicked.connect(self.encontrar_email)
        self.btnLimpiar.clicked.connect(self.limpiar_campos)
        self.btnCerrar.clicked.connect(self.close)
    
    def encontrar_email(self):
        dominio = self.txtDominio.text()
        nombre = self.txtNombre.text()
        apellido = self.txtApellido.text()
        email = encontrar_email(dominio, nombre, apellido)
        if email:
            self.txtEmail.setText(email)

    def limpiar_campos(self):
        self.txtDominio.clear()
        self.txtNombre.clear()
        self.txtApellido.clear()
        self.txtEmail.clear()

class VentanaVerificar(QtWidgets.QMainWindow):
    def __init__(self):
        super(VentanaVerificar, self).__init__()
        uic.loadUi('ventana_verificar.ui', self)
        self.btnVerificar.clicked.connect(self.verificar_email)
        self.btnLimpiar.clicked.connect(self.limpiar_campos)
        self.btnCerrar.clicked.connect(self.close)
    
    def verificar_email(self):
        email = self.txtEmail.text()
        verificar_email(email)

    def limpiar_campos(self):
        self.txtEmail.clear()

app = QtWidgets.QApplication([])
mainWindow = MainWindow()
mainWindow.show()
sys.exit(app.exec_())






