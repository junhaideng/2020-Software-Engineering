import sqlite3
from bbs.course.models import TeacherOfCourse,Course
SCHOOLS = (  # 学院名称
    ("电子信息与电气工程学院", "电子信息与电气工程学院"),
    ("机械与动力工程学院", "机械与动力工程学院"),
    ("船舶海洋与建筑工程学院", "船舶海洋与建筑工程学院"),
    ("生物医学工程学院", "生物医学工程学院"),
    ("航空航天学院", "航空航天学院"),
    ("数学科学院", "数学科学院"),
    ("物理与天文学院", "物理与天文学院"),
    ("化学化工学院", "化学化工学院"),
    ("致远学院", "致远学院"),
    ("医学院", "医学院"),
    ("安泰经济与管理学院", "安泰经济与管理学院"),
    ("人文学院", "人文学院"),
    ("材料科学与工程学院", "材料科学与工程学院"),
    ("海洋学院", "海洋学院"),
    ("药学院", "药学院"),
    ("生命科学技术学院", "生命科学技术学院"),
    ("农业与生物学院", "农业与生物学院"),
    ("凯原法学院", "凯原法学院"),
    ("外国语学院", "外国语学院"),
    ("体育系", "体育系"),
    ("马克思主义学院", "马克思主义学院"),
    ("国际公共与事务学院", "国际公共与事务学院"),
    ("上海高级金融学院", "上海高级金融学院"),
    ("巴黎高科卓越工程师学院", "巴黎高科卓越工程师学院")
)

data=sqlite3.connect("D:/gitRepository/2020-Software-Engineering/data.db")
da=data.cursor()
ret = da.execute("select * from CLASSES")    #获取该表所有元素
# 2 SCHOOL 4 课程名  5 教师  8 选修1 or 必修0
# course_course 1name 2type 3major 4school
# course_teacherofcourse 1 name 2 course_id
no='暂无'
type="CO"
for row in ret:
    print(row[1]) #这里就是获取去除来的每行的第2个元素的内容，row[0]则是第一个
    if row[8] == 1:
        type = "El"
    for i in SCHOOLS:
        if i[0] == row[2]:
            print("1")
            a=Course()
            a.name=row[4]
            a.school=row[2]
            a.major="暂无信息"
            a.type=type
            a.save()
            break
        #(1,"+ row[4] + "," + type + ", " + no + ", " + row[2] + ")
    break
data.close()