from flask import redirect, render_template, url_for, flash, request, Blueprint, current_app
from sqlalchemy import null
from flask_login import current_user, login_required
from banc import db
from banc.models import Project, User, Bids, Ratings
from datetime import datetime
import os
import secrets
from PIL import Image
from flask import current_app

main = Blueprint('main',__name__)

@login_required
@main.route('/browse_jobs')
def browse():
    #  configure today date
    todayDate = str(datetime.today().date())
    currentTime = str(datetime.now().time())
    datePostedStr = todayDate + currentTime
    datePostedObj = datetime.strptime(datePostedStr[0:18], '%Y-%m-%d%H:%M:%S')

    userSkills = []
    for s in current_user.skills:
       userSkills.append(s.skill_name)

    all = Project.query.all() # get all users
    p = [] # in the end, this list will store the users which have an id in the list
   
    # loop through all the users
    for pp in all:
      for s in pp.required_skills.split(','):
         print(s)
         if (s).lower() in userSkills:
            p.append(pp) # if the user's id is in list append to list
            break
         print('......................')
    print(p)
    
# you now have a list of users in list stored in the variable users!
   
    # fetch projects
    page = request.args.get('page',1,type=int)
    #projects = Project.query.order_by(Project.date_posted.desc()).filter(Ssb.user_id == current_user.id).paginate(page=page,per_page=5) 
    projects = Project.query.order_by(Project.date_posted.desc()).paginate(page=page,per_page=5) 
    
    
    return render_template('browse_projects.html',projects=projects,tday=datePostedObj,lUser=current_user,p=p)

@login_required
@main.route('/post-project', methods=['GET','POST'])
def post_project():
    if request.method == 'POST':
       #  configure today date
        todayDate = str(datetime.today().date())
        currentTime = str(datetime.now().time())
        datePostedStr = todayDate + currentTime
        datePostedObj = datetime.strptime(datePostedStr[0:18], '%Y-%m-%d%H:%M:%S')
        d = request.form['deadline'] + currentTime
        print(d,todayDate)
        deadline = datetime.strptime(d[0:18], '%Y-%m-%d%H:%M:%S')
        #details from form
        projectName = request.form['project-name']
        pDesciption = request.form['p-description']
        requiredSkills = request.form['required-skills']
        pType = request.form['p-type']
        currencyy = request.form['currency']
        budget = request.form['budget-range']
        # create project object and save to database
        project = Project(date_posted=datePostedObj,project_name=projectName,project_description=pDesciption,required_skills=requiredSkills,payment_type=pType,currencyy=currencyy,budget=budget,deadline=deadline,user_id=current_user.id)
        
        db.session.add(project)
        db.session.commit()

        return redirect(url_for('main.browse')) 
    return render_template('post_project.html')

# show a single project with specified id
@login_required
@main.route('/project-details/<projectId>', methods=['GET','POST'])
def project_details(projectId):
    #  configure today date
    todayDate = str(datetime.today().date())
    currentTime = str(datetime.now().time())
    datePostedStr = todayDate + currentTime
    datePostedObj = datetime.strptime(datePostedStr[0:18], '%Y-%m-%d%H:%M:%S')
    todayD = datePostedObj
    #send bid details to database
    if request.method == 'POST':
        currencyy = request.form['currency']
        bidVal = request.form['bidVal']
        finish = request.form['finish']
        pType = request.form['p-type']

        bds = Bids(date_posted=datePostedObj,currencyy=currencyy,bidd=bidVal,duration=finish,payment_type=pType,project_id=projectId,user_id=current_user.id)
        db.session.add(bds)
        db.session.commit()

    #details specific to a particular project
    project = Project.query.filter_by(id=projectId).first()
    client = User.query.filter_by(id=project.user_id).first()
    allBids = Bids.query.filter_by(project_id=projectId).all()
    numBids = Bids.query.filter_by(project_id=projectId).count()
    totalBids = 0
    if numBids>0:
      for bid in allBids:
         totalBids += int(bid.bidd)
      avgBid = round(totalBids/numBids)
    else:
      avgBid = 0
    return render_template('project_details.html',lUser=current_user,project=project,client=client,allBids=allBids,numBids=numBids,avgBid=avgBid,todayD=todayD)

#show bids on a specific project
@login_required
@main.route('/project-details/<projectId>/bids', methods=['GET','POST'])
def bids(projectId):
   #  configure today date
   todayDate = str(datetime.today().date())
   currentTime = str(datetime.now().time())
   datePostedStr = todayDate + currentTime
   datePostedObj = datetime.strptime(datePostedStr[0:18], '%Y-%m-%d%H:%M:%S')
   todayD = datePostedObj
    #details specific to a particular project
   project = Project.query.filter_by(id=projectId).first()
   client = User.query.filter_by(id=project.user_id).first()
   # page = request.args.get('page',1,type=int)
   allBids = Bids.query.filter_by(project_id=projectId).all()
   numBids = Bids.query.filter_by(project_id=projectId).count()
   totalBids = 0
   if numBids>0:
      for bid in allBids:
         totalBids += int(bid.bidd)
      avgBid = round(totalBids/numBids)
   else:
      avgBid = 0
   #get users for bids
   users = []
   for b in allBids:
      users.append( User.query.filter_by(id=b.user_id).first())
   

   return render_template('bids.html',lUser=current_user,project=project,avgBid=avgBid,allBids=allBids,numBids=numBids,todayD=todayD,data=zip(users,allBids))

#browse freelancers
@login_required
@main.route('/freelancers', methods=['GET','POST'])
def freelancers():

   if request.method == 'POST':
      print("watttttttttttttttttttttttttttttttttt")
      rating = request.form['rating']   
      freelancer_id = request.form['freelancer_id']
      
      ratings = Ratings(rating=rating,freelancer_id=freelancer_id)
      print(ratings)
      db.session.add(ratings)
      db.session.commit()
      return redirect(url_for('main.freelancers'))

   page = request.args.get('page',1,type=int)
   users = User.query.order_by(User.date_joined.desc()).paginate(page=page,per_page=5) 
   return render_template('freelancers.html',lUser=current_user,users=users)

# route to handle ssb application form
# @login_required
# @main.route('/ssb/application', methods=['GET','POST'])
# def ssbApplication():

#     if request.method == 'POST':
       # configure today date
    #    todayDate = str(datetime.today().date())
    #    currentTime = str(datetime.now().time())
    #    dateAppliedStr = todayDate + currentTime
    #    dateAppliedObj = datetime.strptime(dateAppliedStr[0:18], '%Y-%m-%d%H:%M:%S')
       #convert dates to python dates
    #    startDate = datetime.strptime(request.form['startDate'], '%Y-%m-%d')
    #    endDate = datetime.strptime(request.form['endDate'], '%Y-%m-%d')
       
       #create Ssb object

    #    ssb = Ssb(date_applied=dateAppliedObj,firstname=request.form['firstName'],surname=request.form['surname'],new=request.form['new'],change=request.form['change'],cease=request.form['cease'],
    #               ec_number=request.form['employeeCodeNumber'],c_d=request.form['cd'],payee_code=request.form['payeeCode'],monthly_rate=request.form['monthlyRate'],start_date=startDate,end_date=endDate,
    #                national_id_or_passport=request.form['idPassportNumber'],user_id=current_user.id)
       
       
       
       #add ssb application to database
    #    db.session.add(ssb)
    #    db.session.commit()
       #notify user the application was successful
    #    flash('Successfully Submitted Ssb Application','success2')
    #    return redirect(url_for('main.guide'))   
        
    # return render_template('ssb.html')

