from app import app, db
from app.models import Books, References, Sources, Targets

@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'Books': Books,
            'References': References,
            'Sources': Sources,
            'Targets': Targets
            }