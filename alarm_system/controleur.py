from gpiozero import MotionSensor, Buzzer, LED
from time import sleep
import KeypadGPIO as c
from Adafruit_LCD1602 import Adafruit_CharLCD
from PCF8574 import PCF8574_GPIO
from modele import Model

code = "12345"
touches = ['1', '2', '3', 'A',
           '4', '5', '6', 'B',
           '7', '8', '9', 'C',
           '*', '0', '#', 'D']
lignesGPIO = [18, 23, 24, 25]
colonnesGPIO = [6, 13, 19, 26]

LIGNES = 4
COLONNES = 4

def lcd():
    PCF8574_address = 0x27  
    PCF8574A_address = 0x3F  
    
    try:
        mcp = PCF8574_GPIO(PCF8574_address)
    except:
        try:
            mcp = PCF8574_GPIO(PCF8574A_address)
        except:
            print('I2C Address Error !')
            exit(1)
    
    mcp.output(3, 1)
    lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)
    lcd.begin(16, 2)
    return lcd

class Controller:
    def __init__(self, vue, model):
        self.rouge = LED(27)
        self.greenFn = LED(22)
        self.rouge.on()
        self.vue = vue
        self.vue.set_controller(self)
        self.lcd = lcd()
        self.model = model
        Model.create_table()  
        self.actions = []
        self.pir = MotionSensor(4)
        self.buzzer = Buzzer(5)
        self.pir.when_motion = self.captation
        self.pir_actif = False
        self.clavier = c.Keypad(touches, lignesGPIO, colonnesGPIO, LIGNES, COLONNES)
        self.clavier.setDebounceTime(50)

    def start(self):
        action = Model("activation")
        self.actions.append(action)
        self.vue.ajouter_action(action)

        self.pir_actif = True
        self.lcd.clear()
        self.lcd.message("Systeme active")
        self.rouge.off()
        self.greenFn.on()
        self.vue.desactiver_btn_activer()
        self.vue.update_status_label(True)

    def stop(self):
        action = Model("desactivation")
        self.actions.append(action)
        self.vue.ajouter_action(action)
        self.lcd.clear()
        self.lcd.message("Systeme \ndesactive")
        self.rouge.on()
        self.greenFn.off()
        self.pir_actif = False
        self.vue.activer_btn_activer()
        self.vue.update_status_label(False)

    def captation(self):
        if not self.pir_actif:
            return

        self.lcd.clear()
        self.lcd.message("Entrez le code :")
        self.actions.append(Model("mouvement detecte"))
        self.vue.ajouter_action(self.actions[-1])

        combinaison = ""
        wrong_attempts = 0
        correct_code_entered = False

        while not correct_code_entered:
            touche = self.clavier.getKey()
            if touche != self.clavier.NULL:
                combinaison += touche
                self.lcd.clear()
                self.lcd.message("Votre code:\n")
                self.lcd.message(combinaison)
                self.buzzer.on()
                sleep(0.1)
                self.buzzer.off()

                if combinaison == code:
                    self.vue.activer_btn_desactiver()
                    self.lcd.clear()
                    self.lcd.message("Bon code\n desactiver?")
                    correct_code_entered = True
                    action = Model("code entre, bonne combinaison")
                    self.actions.append(action)
                    self.vue.ajouter_action(action)
                elif len(combinaison) == 5:
                    combinaison = ""
                    wrong_attempts += 1
                    action = Model("code entre, mauvaise combinaison")
                    self.actions.append(action)
                    self.vue.ajouter_action(action)
                    if wrong_attempts == 3:
                        for _ in range(5):
                            self.buzzer.on()
                            self.rouge.on()
                            self.lcd.clear()
                            self.lcd.message("Sortez de \n chez moi")
                            sleep(0.2)
                            self.buzzer.off()
                            self.rouge.off()
                            sleep(0.2)
                        self.shutdown_application()
                        return  
                    else:
                        self.lcd.clear()
                        self.lcd.message("Mauvaise \n combinaison")
                        sleep(1)
                        self.lcd.clear()
                        self.lcd.message("Entrez le code :")
            sleep(0.1)

    def save_actions_to_db(self):
        for action in self.actions:
            action.save_to_db()

    def cleanup(self):
        self.rouge.off()
        self.greenFn.off()
        self.lcd.clear()
        self.pir.when_motion = None

    def shutdown_application(self):
        self.cleanup()
        self.vue.quit_application()
