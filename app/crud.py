from app.database import SessionLocal
from app.models import Tutor, Animal, Atendimento

def popular_banco():
    db = SessionLocal()   
    try:
        if db.query(Tutor).count() > 0:
            print('Banco já preenchido. Pulando...')
            return

        tutor1 = Tutor(
            nome_completo='Thiago Henrique Alves Lima', 
            telefone='61999990001', 
            email='thiago@email.com'
        )
        tutor2 = Tutor(
            nome_completo='Carlos Eduardo', 
            telefone='61988880002', 
            email='carlos@email.com'
        )

        db.add_all([tutor1, tutor2])
        db.flush()  


        animal1 = Animal(
            nome_animal='Rex', 
            especie='cão', 
            raca='Pastor Alemão', 
            peso_kg=28.5, 
            tutor_id=tutor1.id
        )
        animal2 = Animal(
            nome_animal='Mimi', 
            especie='gato', 
            raca='Siamês', 
            peso_kg=4.2, 
            tutor_id=tutor1.id
        )
        animal3 = Animal(
            nome_animal='Loro', 
            especie='ave', 
            raca='Papagaio', 
            peso_kg=0.5, 
            tutor_id=tutor2.id
        )

        db.add_all([animal1, animal2, animal3])
        db.flush() 

        atend1 = Atendimento(
            data_atend='07/10/2026', 
            motivo='Vacina anual V8', 
            valor_cons=150.00, 
            animal_id=animal1.id
        )
        atend2 = Atendimento(
            data_atend='07/10/2026', 
            motivo='Consulta de rotina felina', 
            valor_cons=120.00, 
            animal_id=animal2.id
        )
        atend3 = Atendimento(
            data_atend='07/10/2026', 
            motivo='Corte de asas e check-up', 
            valor_cons=90.00, 
            animal_id=animal3.id
        )

        db.add_all([atend1, atend2, atend3])

        db.commit()     
        print('Banco preenchido com sucesso!')

    except Exception as erro:
        db.rollback()   
        print(f'Erro ao popular banco: {erro}')
    finally:
        db.close()      

if __name__ == '__main__':
    popular_banco()