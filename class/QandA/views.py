from django.shortcuts import render
from .models import Question, Answer
from Profiles.models import Profile
# Create your views here.

def question_list(request):

    questions = Question.objects.order_by("-date")
    seen = [ False for question in questions]

    if request.user.is_anonymous():
        print("\nredirect non logged in user to log in page\n")

    elif request.POST:
        question = Question( question=request.POST["new_question"], op=request.user)
        question.save() #may need to save a special way

        #update each user to mark the question as unread
        for user in Profile.objects.all():
            user.questions.add(question)


        questions = Question.objects.order_by("-date")

    seen = []
    #build list of true/false values to determine if the user has read the question
    if request.user.is_authenticated():

        user = Profile.objects.get( user=request.user)
        for question in questions:
            seen.append(question in user.questions.all())



    #bind question to seen or not
    questions = [(question, has_seen) for question, has_seen in zip(questions, seen)]

    return render(request, 'QandA/listview.html', {'questions': questions})


def detail_view(request, pk):

    #get the question
    question = Question.objects.get(pk=pk)
    try:
        answers = Answer.objects.filter( question=question).order_by('date') #get all answers to question


    except:
        answers = []

    if not request.user.is_authenticated:
        print('\n\nRedirect user to login')
    elif request.POST:
        answer = Answer( response=request.POST['answer'], op=request.user, question=question)

        answer.save()

        #update each user to mark the question as unread
        for user in Profile.objects.all():
            user.answers.add(answer)

        #answers = Answer.objects.filter(question=question).sort_by('date')
        answers = Answer.objects.filter(question=question).order_by('date') #get all answers to question






    #remove all answers and question from user list
    if request.user.is_authenticated():
        user = Profile.objects.get(user=request.user)
        user.questions.remove(question)
        for a in answers:
            user.answers.remove(a)



    return render(request, 'QandA/detailview.html', {'question': question, 'answers': answers})

'''
def update_Qlist(request):

    q = Question( question = request.POST['new_question'])


    q.save()
    questions = Question.objects.order_by("-date")


    request.path = 'question/'



    return render(request, 'QandA/listview.html', {'questions':questions})
'''
