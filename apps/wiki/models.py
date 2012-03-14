# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
GRADE_LEVEL_CHOICE = (
                      ('KINDERGARTEN','Kindergarten/Pre-K'),
                      ('1G','1st Grade'),
                      ('2G','2nd Grade'),
                      ('3G','3rd Grade'),
                      ('4G','4th Grade'),
                      ('5G','5th Grade'),
                      ('6G','6th Grade'),
                      ('7G','7th Grade'),
                      ('8G','8th Grade'),
                      ('9G','9th Grade'),
                      ('10G','10th Grade'),
                      ('11G','11th Grade'),
                      ('12G','12th Grade'),
                      ('COLLEGE','College'),
                      ('OCCUPTIONAL','Occupational'))
SUBJECT_CHOICE = (
					('ART','Art'),
					("BUSINESSECOMOMICS",'Business and Economics'),
					('COMPUTERSCIENCE','Computer Science'),
					('GEOGRAPHY','Geography'),
					('History',(
								('CHINA','China'),
								('VIETNAM',u'Việt Nam'),
								('WORLD', 'World'),
								)
					),
					('MUSIC','Music'),
					('MOVE','Move'),
					('Math',(
								('ALEGEBRA','Alegebra'),
								('ARITHMETIC','Arithmetic'),
								('CALCULUS', 'Calculus'),
								('GEOMETRY','Geometry'),
								('STATISTICS', 'Statistics'),
								)
					),
					('Foreign Language',(
								('ENGLISH','English'),
								('VIETNAMESE','Vietnamese'),
								('CHINESE', 'Chinese'),
								('SPANISH','Spanish'),
								)
					),
					
					('Sience',(
								('BIOLoGY','Biology'),
								('CHEMISTRY','Chemistry'),
								('EARTHSICENCE', 'Earth Science'),
								('PHYSICS','Physics'),
								('PSYCHOLOGY', 'Psychology'),
								('MEDICINE','Medicine'),
								)
					),
					('RELIGION','Religion'),
					('OTHER','Other')
				)    
LESSON_TYPE_CHOICE = (
                      ('TEACHER','Teacher Lesson Plan'),
                      ('STUDENT','Student Study Guide'),
                      ('ASSIGNMENT','Assignment/Project'),
                      ('CLASSROOM_INFORMATION','Classroom Information'),
                	  ('OTHER','Other')
)
	
class Wiki(models.Model):
	user = models.ForeignKey(User, related_name = 'user')
	title = models.CharField('Title',max_length = 40)
	titleid = models.CharField('Title ID',max_length = 40, primary_key = True)
	description = models.CharField('Description', max_length = 400)
	gradelevel = models.CharField('Grade Level', choices = GRADE_LEVEL_CHOICE, max_length = 20)
	subject = models.CharField('Subsject', choices = SUBJECT_CHOICE, max_length = 30)
	lessontype = models.CharField('Lesson Type', choices = LESSON_TYPE_CHOICE, max_length = 30)
	like = models.IntegerField(default = 0)
	userlike = models.ManyToManyField(User,blank=True,null=True)
	def __unicode__(self):
		return self.title
class PageOne(models.Model):
	parent = models.ForeignKey(Wiki)
	title = models.CharField('Title', max_length = 40, primary_key = True)
	titleid = models.CharField('Title ID', max_length = 40)
	def __unicode__(self):
		return self.title
class PageTwo(models.Model):
	parent = models.ForeignKey(PageOne)
	title = models.CharField('Title', max_length = 40, primary_key = True)
	titleid = models.CharField('Title ID', max_length = 40)
	def __unicode__(self):
		return self.title
class Section(models.Model):
	wiki = models.ManyToManyField(Wiki)
	pageone = models.ManyToManyField(PageOne)
	pagetwo = models.ManyToManyField(PageTwo)
	title = models.CharField('Title', max_length = 40)
	content = models.TextField("Content",error_messages={'blank': 'NotNull','required': "My custom error"})
	content_markdown = models.TextField("Content Markdown")
	def __unicode__(self):
		return self.title
	def save(self, *args, **kargs):
		import markdown
		md = markdown.Markdown(extensions =
								['wikilinks','mdx_video','urlize',
									'nl2br','addsections',
								],
							   safe_mode = "escape"
							  )
		self.content_markdown = md.convert(self.content)
		super(Section,self).save(*args, **kargs)
class Image(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField('Title', max_length = 40)
	photo = models.ImageField(upload_to = 'photos')
	def __unicode__(self):
		return self.title