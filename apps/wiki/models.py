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
                  ('MATH','Math'),
                  ('ART','Art'),
                  ('SCIENCE','Science'))

LESSON_TYPE_CHOICE = (
                      ('TEACHER','Teacher Lesson Plan'),
                      ('STUDENT','Student Study Guide'),
                      ('ASSIGNMENT','Assignment/Project'),
                      ('CLASSROOM_INFORMATION','Classroom Information'),
                      ('OTHER','Other'))
class Wiki(models.Model):
	user = models.ForeignKey(User)
	wiki_title = models.CharField('Title',max_length = 40)
	wiki_description = models.CharField('Description', max_length = 100)
	wiki_gradeLevel = models.CharField('Grade Level', choices = GRADE_LEVEL_CHOICE, max_length = 20)
	wiki_subject = models.CharField('Subsject', choices = SUBJECT_CHOICE, max_length = 30)
	wiki_lessonType = models.CharField('Lesson Type', choices = LESSON_TYPE_CHOICE, max_length = 30)
	wiki_like = models.IntegerField()
	def __unicode__(self):
		return self.wiki_title
class Section(models.Model):
	wiki = models.ForeignKey(Wiki)
	sec_title = models.CharField('Title', max_length = 40)
	sec_content = models.TextField("Content")
	def __unicode__(self):
		return self.sec_title
	
