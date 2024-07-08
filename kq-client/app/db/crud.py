from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas
import uuid


def get_job(db: Session, jobStatus: schemas.JobUUID) -> models.Jobs:
    return db.query(models.Jobs).filter(models.Jobs.uuid == jobStatus.uuid).first()


def delete_job(db: Session, jobStatus: schemas.JobUUID):
    db_job = (
        db.execute(select(models.Jobs).filter(models.Jobs.uuid == jobStatus.uuid))
        .scalars()
        .first()
    )
    if db_job:
        db.delete(db_job)
        db.commit()
        return True
    else:
        return False


def update_job_status(db: Session, jobStatus: schemas.JobUpdateStatus):
    job = (
        db.query(models.Jobs)
        .filter(models.Jobs.uuid == jobStatus.uuid)
        .update({"status": jobStatus.status})
    )
    db.commit()
    if job:
        return True
    else:
        return False


def update_job_result(db: Session, jobOutputObj: schemas.JobUpdateResultfile):
    job = (
        db.query(models.Jobs)
        .filter(models.Jobs.uuid == jobOutputObj.uuid)
        .update(
            {"status": jobOutputObj.status, "result_file": jobOutputObj.result_file}
        )
    )
    db.commit()
    if job:
        return True
    else:
        return False


def create_job(db: Session, job: schemas.JobCreate) -> models.Jobs:
    db_job = models.Jobs(
        type=job.type,
        status="Created",
        shot=job.shot,
        input_file=job.input_file,
        uuid=str(uuid.uuid4()),
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return db_job
