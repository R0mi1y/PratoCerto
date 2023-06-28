from django_cron import CronJobBase, Schedule
from django_cron import CronJobBase, Schedule
from datetime import datetime

class MinhaTarefaAgendada(CronJobBase):
    RUN_AT_TIMES = ['22:00']  # Horário desejado para executar a tarefa
    DATE_TO_RUN = datetime(2023, 7, 1)  # Data específica para executar a tarefa

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'meuapp.minha_tarefa_agendada'    # Nome da tarefa

    def do(self):
        # Verificar se a data atual é igual à data desejada
        if datetime.now().date() == self.DATE_TO_RUN.date():
            pass
