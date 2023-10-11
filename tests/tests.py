import pytest
from pmgr.project import Project, TaskException
from pathlib import Path


@pytest.fixture(scope="function")
def testproj():
    tproj = Project('mytestproj')
    yield tproj
    tproj.delete()

def test_add_to_nonproject():
    with pytest.raises(TaskException):
       testproj = Project('mytestproj')
       testproj.delete()
       testproj.add_task('task')

def test_remove_from_nonproject():
    with pytest.raises(TaskException):
       testproj = Project('mytestproj')
       testproj.delete()
       testproj.remove_task('nothing')

def test_add(testproj):
    testproj.add_task('dosomething')
    assert 'dosomething' in testproj.get_tasks()

def test_remove(testproj):
    testproj.add_task('something')
    testproj.remove_task('something')
    assert 'something' not in testproj.get_tasks()

def test_invisible_task(testproj):
    with pytest.raises(TaskException):
       testproj.remove_task('invisible_task')

def test_get_empty_list(testproj):
    task_list = testproj.get_tasks()
    assert len(task_list) == 0

def test_get_list(testproj):
    testproj.add_task('something')
    testproj.add_task("another_something")
    task_list = testproj.get_tasks()
    assert 'something' and 'another_something' in task_list

def test_large_numbers(testproj):
    for i in range(1000):
       testproj.add_task(f'something_{i}')
    task_list = testproj.get_tasks()
    assert len(task_list) == 1000

def test_manipulation(testproj):
    testproj.add_task('nothing')
    testproj.add_task('task1')
    testproj.remove_task('nothing')
    testproj.add_task('task2')
    testproj.remove_task('task1')
    testproj.remove_task('task2')
    task_list = testproj.get_tasks()
    assert len(task_list) == 0

def test_deleting_full_proj():
    testproj = Project('project')
    testproj.add_task('task')
    testproj.add_task('task1')
    testproj.add_task('task2')
    testproj.delete()

def test_tasks_same_name(testproj):
    with pytest.raises(TaskException):
       testproj.add_task('task1')
       testproj.add_task('task1')
