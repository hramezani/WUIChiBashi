import uuid
import json
import subprocess
from shlex import quote
from pathlib import Path

from flask import Blueprint, flash, render_template
from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, FormField, validators
from flask_simplelogin import login_required


bp = Blueprint('entryPoint', __name__)


# straight from the wtforms docs:
class HostForm(FlaskForm):
    fullName = TextField('Host IP/Name', [validators.required()])


class ExampleForm(FlaskForm):
    # subforms
    new_Host = FormField(HostForm)
    submit_button = SubmitField('Run')


@bp.route('/', methods=('GET', 'POST'))
@login_required  # < --- simple decorator
def index():
    """TODO"""
    form = ExampleForm()
    runningProgramID = ''
    if form.validate_on_submit():
        host = form.new_Host.fullName.data
        flash('Requested for {}'. format(host))
        tmpFileName = str(uuid.uuid4())
        if runCommand(host, tmpFileName) == 0:
            runningProgramID = tmpFileName
        else:
            flash('Some Errors happend!', 'error')
    else:
        if form.errors:
            print(form.errors)
    return render_template('entryPoint/index.html', form=form,
                           runningProgramID=runningProgramID)


@bp.route('/checkStatus/<string:id>')
@login_required
def checkStatus(id):
    """TODO"""
    fileFullAddress = '/tmp/' + id
    file = open(fileFullAddress, 'r')
    content = file.read()
    result = {}
    result['content'] = content
    path = Path(fileFullAddress + '.finished')
    if path.exists():
        result['status'] = 'finished'
    else:
        result['status'] = 'running'
    return json.dumps(result)


def runCommand(host, tmpFileName):
    """TODO"""
    # Attention: Sanitizing inputs MUST be done
    host = quote(host)

    path = str(Path().absolute())
    worker_path = path + '/worker.py'

    return subprocess.call(['python', worker_path, host, tmpFileName])
