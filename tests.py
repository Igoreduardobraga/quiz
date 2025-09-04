import pytest
from model import Question


@pytest.fixture
def question_with_choices():
    q = Question(title="Capital do Brasil", max_selections=2)
    q.add_choice("Rio de Janeiro")
    q.add_choice("São Paulo")        
    q.add_choice("Brasília")         
    q.set_correct_choices([3])
    return q

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct
    

def test_add_multiple_choices_assigns_incremental_ids():
    q = Question(title='q1')
    c1 = q.add_choice('A')
    c2 = q.add_choice('B')
    c3 = q.add_choice('C')
    assert [c.id for c in q.choices] == [1, 2, 3]


def test_add_choice_with_invalid_text_raises():
    q = Question(title='q1')
    with pytest.raises(Exception):
        q.add_choice('')
    with pytest.raises(Exception):
        q.add_choice('x' * 101)


def test_remove_choice_by_id_removes_that_choice():
    q = Question(title='q1')
    q.add_choice('A')
    q.add_choice('B')
    q.remove_choice_by_id(1)
    assert [c.id for c in q.choices] == [2]
    assert q.choices[0].text == 'B'


def test_remove_choice_by_id_with_invalid_id_raises():
    q = Question(title='q1')
    q.add_choice('A')
    with pytest.raises(Exception):
        q.remove_choice_by_id(99)


def test_choice_id_resets_after_remove_all():
    q = Question(title='q1')
    q.add_choice('A')
    q.add_choice('B')
    q.remove_all_choices()
    c = q.add_choice('C')
    assert c.id == 1


def test_set_correct_choices_marks_specified_as_correct():
    q = Question(title='q1')
    q.add_choice('A')  
    q.add_choice('B')  
    q.add_choice('C')  
    q.set_correct_choices([2, 3])
    assert [c.id for c in q.choices if c.is_correct] == [2, 3]


def test_set_correct_choices_with_invalid_id_raises_and_keeps_prior_changes():
    q = Question(title='q1')
    q.add_choice('A')  
    q.add_choice('B')  
    with pytest.raises(Exception):
        q.set_correct_choices([1, 999])
    assert q._find_correct_choice_ids() == [1]


def test_correct_selected_choices_returns_only_correct():
    q = Question(title='q1')
    q.add_choice('A')  # 1
    q.add_choice('B')  # 2
    q.set_correct_choices([2])

    assert q.correct_selected_choices([1]) == []

    assert q.correct_selected_choices([2]) == [2]


def test_correct_selected_choices_enforces_max_selections():
    q = Question(title='q1', max_selections=1)
    q.add_choice('A')  
    q.add_choice('B')  
    with pytest.raises(Exception):
        q.correct_selected_choices([1, 2])


def test_correct_selected_choices_allows_multiple_when_configured():
    q = Question(title='q1', max_selections=2)
    q.add_choice('A')  
    q.add_choice('B')  
    q.add_choice('C')  
    q.set_correct_choices([1, 3])
    result = q.correct_selected_choices([1, 3])
    assert result == [1, 3]
    

def test_fixture_question_has_expected_choices(question_with_choices):
    texts = [c.text for c in question_with_choices.choices]
    assert texts == ["Rio de Janeiro", "São Paulo", "Brasília"]
    assert question_with_choices.points == 1


def test_fixture_question_correct_answer(question_with_choices):
    result = question_with_choices.correct_selected_choices([1, 3])
    assert result == [3]