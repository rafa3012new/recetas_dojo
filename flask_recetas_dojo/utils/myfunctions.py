import datetime


def diferencia_tiempo(tiempo1,tiempo2):

  #CONSTANTS
  DURACION_SEGUNDOS_1HORA = 3600
  DURACION_SEGUNDOS_1DIA = 86400
  DURACION_SEGUNDOS_1SEMANA = 604800
  DURACION_SEGUNDOS_1MES = 2592000
  DURACION_SEGUNDOS_1ANO = 31536000

  #Variables
  duration = 0
  cadena_duracion = ""

  #Initial Calculation
  duration = tiempo2 - tiempo1
  print(duration,flush=True)
#   total_segundos = duration.seconds()

  #Faltaria calcular con biciesto y meses de 30 y 31
  # exacto con ano biciesto

#   if  (total_segundos // DURACION_SEGUNDOS_1ANO) > 0:
#       cadena_duracion += str(total_segundos // DURACION_SEGUNDOS_1ANO) + "Anos"
#       total_segundos-= (total_segundos // DURACION_SEGUNDOS_1MES) * DURACION_SEGUNDOS_1ANO
#   elif (total_segundos // DURACION_SEGUNDOS_1MES) > 0:
#       cadena_duracion += str(total_segundos // DURACION_SEGUNDOS_1MES)  + "Meses"
#       total_segundos-= (total_segundos // DURACION_SEGUNDOS_1MES) * DURACION_SEGUNDOS_1MES
#   elif (total_segundos // DURACION_SEGUNDOS_1SEMANA) > 0:
#       cadena_duracion += str(total_segundos // DURACION_SEGUNDOS_1SEMANA)  + "Semanas"
#       total_segundos-= (total_segundos // DURACION_SEGUNDOS_1SEMANA) * DURACION_SEGUNDOS_1SEMANA
#   elif (total_segundos // DURACION_SEGUNDOS_1DIA) > 0:
#       cadena_duracion += str(total_segundos // DURACION_SEGUNDOS_1DIA)  + "Dias"
#       total_segundos-= (total_segundos // DURACION_SEGUNDOS_1DIA) * DURACION_SEGUNDOS_1DIA
#   elif (total_segundos // DURACION_SEGUNDOS_1HORA) > 0:
#       cadena_duracion += str(total_segundos // DURACION_SEGUNDOS_1HORA)  + "Horas"
#       total_segundos-= (total_segundos // DURACION_SEGUNDOS_1HORA) * DURACION_SEGUNDOS_1HORA
#   elif (total_segundos // 60) > 0:
#       cadena_duracion += str(total_segundos //60)  + "Minutos"
#       total_segundos-= (total_segundos //   60) * 60
#   elif  total_segundos > 0:
#       cadena_duracion += total_segundos  + "Segundos"
#       # total_segundos-= total_segundos

  return str(duration)
