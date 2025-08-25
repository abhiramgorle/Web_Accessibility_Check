import streamlit as st
import requests
import pandas as pd
import json
import time
import re
from urllib.parse import quote
import logging
from io import BytesIO
import base64

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# JSON data for UF Education Programs
UF_PROGRAMS_DATA = {
  "uf_education_programs": [
    {
      "name": "Computer Science Education",
      "main_url": "https://education.ufl.edu/computer-science-education/",
      "pages": [
        "https://education.ufl.edu/computer-science-education/",
        "https://education.ufl.edu/computer-science-education/program-faculty/",
        "https://education.ufl.edu/computer-science-education/contact-us/",
        "https://education.ufl.edu/computer-science-education/prospective-students/",
        "https://education.ufl.edu/computer-science-education/prospective-students/online-mae/",
        "https://education.ufl.edu/computer-science-education/prospective-students/online-mae/faq/",
        "https://education.ufl.edu/computer-science-education/prospective-students/online-mae/application/",
        "https://education.ufl.edu/computer-science-education/prospective-students/online-ed-d/",
        "https://education.ufl.edu/computer-science-education/prospective-students/online-ed-d/faq/",
        "https://education.ufl.edu/computer-science-education/prospective-students/online-ed-d/online-ed-d-cohort/",
        "https://education.ufl.edu/computer-science-education/prospective-students/computer-science-k-12-teaching-graduate-certificate/application/",
        "https://education.ufl.edu/computer-science-education/prospective-students/computer-science-k-12-teaching-graduate-certificate/",
        "https://education.ufl.edu/computer-science-education/prospective-students/computer-science-k-12-teaching-graduate-certificate/faq"
      ]
    },
    {
      "name": "SITE",
      "main_url": "https://education.ufl.edu/site/",
      "pages": [
        "https://education.ufl.edu/site/",
        "https://education.ufl.edu/site/admission-requirements/",
        "https://education.ufl.edu/site/contact-us/",
        "https://education.ufl.edu/site/degrees/",
        "https://education.ufl.edu/site/faq/",
        "https://education.ufl.edu/site/feed/",
        "https://education.ufl.edu/site/student-experience/"
      ]
    },
    {
      "name": "ESOL/Bilingual Education",
      "main_url": "https://education.ufl.edu/esol/",
      "pages": [
        "https://education.ufl.edu/esol/",
        "https://education.ufl.edu/esol/contact/",
        "https://education.ufl.edu/esol/degrees/",
        "https://education.ufl.edu/esol/degrees/certificate",
        "https://education.ufl.edu/esol/faq/",
        "https://education.ufl.edu/esol/feed/",
        "https://education.ufl.edu/esol/testimonials/"
      ]
    },
    {
      "name": "Counselor Education",
      "main_url": "https://education.ufl.edu/counselor-education/",
      "pages": [
        "https://education.ufl.edu/counselor-education/",
        "https://education.ufl.edu/counselor-education/comments/feed/",
        "https://education.ufl.edu/counselor-education/contact-us/",
        "https://education.ufl.edu/counselor-education/doctoral/",
        "https://education.ufl.edu/counselor-education/feed/",
        "https://education.ufl.edu/counselor-education/program-highlights/",
        "https://education.ufl.edu/counselor-education/prospective-students/",
        "https://education.ufl.edu/counselor-education/prospective-students/on-campus-ph-d/",
        "https://education.ufl.edu/counselor-education/prospective-students/on-campus-ph-d/application/",
        "https://education.ufl.edu/counselor-education/prospective-students/on-campus-ph-d/faq/"
      ]
    },
    {
      "name": "Early Childhood Education",
      "main_url": "https://education.ufl.edu/early-childhood/",
      "pages": [
        "https://education.ufl.edu/early-childhood/",
        "https://education.ufl.edu/early-childhood/admissions/",
        "https://education.ufl.edu/early-childhood/bachelors/",
        "https://education.ufl.edu/early-childhood/contact-us/",
        "https://education.ufl.edu/early-childhood/degrees/",
        "https://education.ufl.edu/early-childhood/early-childhood-certificate",
        "https://education.ufl.edu/early-childhood/early-childhood-studies-undergrad-minor/",
        "https://education.ufl.edu/early-childhood/feed/",
        "https://education.ufl.edu/early-childhood/graduate-certificate",
        "https://education.ufl.edu/early-childhood/minor",
        "https://education.ufl.edu/early-childhood/traditional-early-childhood-masters-degree/",
        "https://education.ufl.edu/etc/a-to-z-of-early-childhood/"
      ]
    },
    {
      "name": "Educational Technology",
      "main_url": "https://education.ufl.edu/educational-technology/",
      "pages": [
        "https://education.ufl.edu/educational-technology/",
        "https://education.ufl.edu/educational-technology/2024/03/07/composite-mentoring-for-graduate-students/",
        "https://education.ufl.edu/educational-technology/2024/03/15/career-options/",
        "https://education.ufl.edu/educational-technology/2024/05/06/student-education-technology-research/",
        "https://education.ufl.edu/educational-technology/contact-us/",
        "https://education.ufl.edu/educational-technology/prospective-students/",
        "https://education.ufl.edu/educational-technology/prospective-students/baes-specialization/",
        "https://education.ufl.edu/educational-technology/prospective-students/graduate-certificate/",
        "https://education.ufl.edu/educational-technology/prospective-students/graduate-certificate/application",
        "https://education.ufl.edu/educational-technology/prospective-students/graduate-certificate/faq",
        "https://education.ufl.edu/educational-technology/prospective-students/on-campus-mae/",
        "https://education.ufl.edu/educational-technology/prospective-students/on-campus-mae/application",
        "https://education.ufl.edu/educational-technology/prospective-students/on-campus-mae/faq",
        "https://education.ufl.edu/educational-technology/prospective-students/on-campus-phd/",
        "https://education.ufl.edu/educational-technology/prospective-students/on-campus-phd/application",
        "https://education.ufl.edu/educational-technology/prospective-students/on-campus-phd/faq/",
        "https://education.ufl.edu/educational-technology/prospective-students/online-edd/",
        "https://education.ufl.edu/educational-technology/prospective-students/online-edd/application",
        "https://education.ufl.edu/educational-technology/prospective-students/online-edd/faq",
        "https://education.ufl.edu/educational-technology/prospective-students/online-eds/",
        "https://education.ufl.edu/educational-technology/prospective-students/online-eds/application",
        "https://education.ufl.edu/educational-technology/prospective-students/online-eds/faq",
        "https://education.ufl.edu/educational-technology/prospective-students/online-edtech-41/",
        "https://education.ufl.edu/educational-technology/prospective-students/online-med/",
        "https://education.ufl.edu/educational-technology/prospective-students/online-med/application",
        "https://education.ufl.edu/educational-technology/prospective-students/online-med/faq",
        "https://education.ufl.edu/educational-technology/prospective-students/undergraduate-minor/"
      ]
    },
    {
      "name": "Educational Leadership",
      "main_url": "https://education.ufl.edu/educational-leadership/",
      "pages": [
        "https://education.ufl.edu/educational-leadership/",
        "https://education.ufl.edu/educational-leadership/contact-us/",
        "https://education.ufl.edu/educational-leadership/program-highlight/",
        "https://education.ufl.edu/educational-leadership/prospective-students/",
        "https://education.ufl.edu/educational-leadership/prospective-students/blended-edd/",
        "https://education.ufl.edu/educational-leadership/prospective-students/ed-s/",
        "https://education.ufl.edu/educational-leadership/prospective-students/ed-s/application/",
        "https://education.ufl.edu/educational-leadership/prospective-students/ed-s/faq/",
        "https://education.ufl.edu/educational-leadership/prospective-students/on-campus-m-ed/",
        "https://education.ufl.edu/educational-leadership/prospective-students/on-campus-m-ed/application/",
        "https://education.ufl.edu/educational-leadership/prospective-students/on-campus-m-ed/faq/",
        "https://education.ufl.edu/educational-leadership/prospective-students/on-campus-ph-d/",
        "https://education.ufl.edu/educational-leadership/prospective-students/on-campus-ph-d/application",
        "https://education.ufl.edu/educational-leadership/prospective-students/on-campus-ph-d/faq/",
        "https://education.ufl.edu/educational-leadership/prospective-students/online-ed-d/",
        "https://education.ufl.edu/educational-leadership/prospective-students/online-ed-d/application/",
        "https://education.ufl.edu/educational-leadership/prospective-students/online-ed-d/faq/",
        "https://education.ufl.edu/educational-leadership/prospective-students/online-m-ed-systems-leadership-track/",
        "https://education.ufl.edu/educational-leadership/prospective-students/online-m-ed/",
        "https://education.ufl.edu/educational-leadership/prospective-students/online-m-ed/application",
        "https://education.ufl.edu/educational-leadership/prospective-students/online-m-ed/faq/",
        "https://education.ufl.edu/educational-leadership/prospective-students/online-med/",
        "https://education.ufl.edu/educational-leadership/webinar-uf-ed-leadership-and-policy/"
      ]
    },
    {
      "name": "Education Sciences",
      "main_url": "http://education.ufl.edu/education-sciences",
      "pages": [
        "http://education.ufl.edu/education-sciences",
        "https://education.ufl.edu/education-sciences/contact-us/",
        "https://education.ufl.edu/education-sciences/program-highlights/",
        "https://education.ufl.edu/education-sciences/prospective-students/",
        "https://education.ufl.edu/education-sciences/prospective-students/on-campus-b-a/",
        "https://education.ufl.edu/education-sciences/prospective-students/online-b-a/"
      ]
    },
    {
      "name": "Elementary Education",
      "main_url": "https://education.ufl.edu/elementary-education/",
      "pages": [
        "https://education.ufl.edu/elementary-education/",
        "https://education.ufl.edu/elementary-education/bachelors/",
        "https://education.ufl.edu/elementary-education/contact/",
        "https://education.ufl.edu/elementary-education/online-bae/"
      ]
    },
    {
      "name": "English Education",
      "main_url": "https://education.ufl.edu/english-education/",
      "pages": [
        "https://education.ufl.edu/english-education/",
        "https://education.ufl.edu/english-education/admissions/",
        "https://education.ufl.edu/english-education/contact-us",
        "https://education.ufl.edu/english-education/team/",
        "https://education.ufl.edu/english-education/courses/",
        "https://education.ufl.edu/english-education/degrees/",
        "https://education.ufl.edu/english-education/degrees/certificate/",
        "https://education.ufl.edu/english-education/degrees/doctorate/",
        "https://education.ufl.edu/english-education/degrees/masters/",
        "https://education.ufl.edu/english-education/degrees/specialist/",
        "https://education.ufl.edu/english-education/degrees/teacher-certification/",
        "https://education.ufl.edu/english-education/specializations/",
        "https://education.ufl.edu/english-education/specializations/media-literacy-education/"
      ]
    },
    {
      "name": "Higher Education",
      "main_url": "https://education.ufl.edu/higher-education",
      "pages": [
        "https://education.ufl.edu/higher-education",
        "https://education.ufl.edu/higher-education/contact/",
        "https://education.ufl.edu/higher-education/faculty-and-staff/",
        "https://education.ufl.edu/higher-education/hybrid-ed-d-program-of-study/",
        "https://education.ufl.edu/higher-education/program-highlights/",
        "https://education.ufl.edu/higher-education/prospective-students/",
        "https://education.ufl.edu/higher-education/prospective-students/hybrid-edd/",
        "https://education.ufl.edu/higher-education/prospective-students/hybrid-edd/application-instructions/",
        "https://education.ufl.edu/higher-education/prospective-students/hybrid-edd/faq/",
        "https://education.ufl.edu/higher-education/prospective-students/on-campus-med/",
        "https://education.ufl.edu/higher-education/prospective-students/on-campus-med/application-instructions/",
        "https://education.ufl.edu/higher-education/prospective-students/on-campus-med/events/",
        "https://education.ufl.edu/higher-education/prospective-students/on-campus-med/faq/",
        "https://education.ufl.edu/higher-education/prospective-students/on-campus-med/on-campus-med-coursework/",
        "https://education.ufl.edu/higher-education/prospective-students/on-campus-phd/",
        "https://education.ufl.edu/higher-education/prospective-students/on-campus-phd/application-instructions/",
        "https://education.ufl.edu/higher-education/prospective-students/on-campus-phd/faq/",
        "https://education.ufl.edu/higher-education/prospective-students/online-med/",
        "https://education.ufl.edu/higher-education/prospective-students/online-med/application-instructions/",
        "https://education.ufl.edu/higher-education/prospective-students/online-med/faq/"
      ]
    },
    {
      "name": "Mathematics Education",
      "main_url": "https://education.ufl.edu/math-education/",
      "pages": [
        "https://education.ufl.edu/math-education/",
        "https://education.ufl.edu/math-education/certificate/",
        "https://education.ufl.edu/math-education/contact/",
        "https://education.ufl.edu/math-education/doctorate/",
        "https://education.ufl.edu/math-education/doctorate/admissions",
        "https://education.ufl.edu/math-education/doctorate/courses",
        "https://education.ufl.edu/math-education/doctorate/dissertations/",
        "https://education.ufl.edu/math-education/doctorate/recent-graduates/",
        "https://education.ufl.edu/math-education/doctorate/research/",
        "https://education.ufl.edu/math-education/faculty-contact/",
        "https://education.ufl.edu/math-education/masters-2/",
        "https://education.ufl.edu/math-education/students/"
      ]
    },
    {
      "name": "Reading and Literacy Education",
      "main_url": "https://education.ufl.edu/reading-education/",
      "pages": [
        "https://education.ufl.edu/reading-education/",
        "https://education.ufl.edu/reading-education/admissions/",
        "https://education.ufl.edu/reading-education/contact-us/",
        "https://education.ufl.edu/reading-education/course-registration/",
        "https://education.ufl.edu/reading-education/doctorate/",
        "https://education.ufl.edu/reading-education/masters/",
        "https://education.ufl.edu/reading-education/reading-endorsement/",
        "https://education.ufl.edu/reading-education/specialist/",
        "https://education.ufl.edu/reading-education/testimonials/"
      ]
    },
    {
      "name": "Research and Evaluation Methodology",
      "main_url": "https://education.ufl.edu/research-evaluation-methods/",
      "pages": [
        "https://education.ufl.edu/research-evaluation-methods/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/minor/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/on-campus-mae/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/on-campus-mae/application-instructions/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/on-campus-mae/faq/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/on-campus-mae/on-campus-mae-program-course-requirements/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/on-campus-med/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/on-campus-med/application-instructions/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/on-campus-med/faq/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/on-campus-med/on-campus-med-program-course-requirements/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/on-campus-phd/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/on-campus-phd/application-instructions/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/on-campus-phd/faq/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/on-campus-phd/qualitative-specialization/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/on-campus-phd/quantitative-specialization/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/online-mae/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/online-mae/application-instructions/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/online-mae/contact/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/online-mae/faq/",
        "https://education.ufl.edu/research-evaluation-methods/prospective-students/online-med/",
        "https://education.ufl.edu/research-evaluation-methods/research-and-evaluation-methodology-major/courses/",
        "https://education.ufl.edu/research-evaluation-methods/resources/"
      ]
    },
    {
      "name": "School Psychology",
      "main_url": "https://education.ufl.edu/school-psychology/",
      "pages": [
        "https://education.ufl.edu/school-psychology/",
        "https://education.ufl.edu/school-psychology/accreditation/",
        "https://education.ufl.edu/school-psychology/contact/",
        "https://education.ufl.edu/school-psychology/faculty-and-staff/",
        "https://education.ufl.edu/school-psychology/program-highlights/",
        "https://education.ufl.edu/school-psychology/prospective-students/",
        "https://education.ufl.edu/school-psychology/prospective-students/on-campus-eds",
        "https://education.ufl.edu/school-psychology/prospective-students/on-campus-eds/",
        "https://education.ufl.edu/school-psychology/prospective-students/on-campus-eds/application-instructions/",
        "https://education.ufl.edu/school-psychology/prospective-students/on-campus-eds/faq/",
        "https://education.ufl.edu/school-psychology/prospective-students/on-campus-phd",
        "https://education.ufl.edu/school-psychology/prospective-students/on-campus-phd/",
        "https://education.ufl.edu/school-psychology/prospective-students/on-campus-phd/application-instructions/",
        "https://education.ufl.edu/school-psychology/prospective-students/on-campus-phd/faq/"
      ]
    },
    {
      "name": "Science Education",
      "main_url": "https://education.ufl.edu/science-education/",
      "pages": [
        "https://education.ufl.edu/science-education/",
        "https://education.ufl.edu/science-education/2020/07/14/new-nsf-funding-for-julie-browns-team-to-study-biology-instruction/",
        "https://education.ufl.edu/science-education/2021/08/16/nsf-funding-for-julie-browns-team-to-study-culturally-responsive-practice-craft/",
        "https://education.ufl.edu/science-education/certificate/",
        "https://education.ufl.edu/science-education/contact-us/",
        "https://education.ufl.edu/science-education/degree-programs/",
        "https://education.ufl.edu/science-education/doctor-of-philosophy/",
        "https://education.ufl.edu/science-education/education-specialist/",
        "https://education.ufl.edu/science-education/frequently-asked-questions/",
        "https://education.ufl.edu/science-education/master-of-arts/",
        "https://education.ufl.edu/science-education/students/",
        "https://education.ufl.edu/science-education/students/dissertations/",
        "https://education.ufl.edu/science-education/students/testimonials/"
      ]
    },
    {
      "name": "Science or Mathematics Teaching Certificate",
      "main_url": "https://education.ufl.edu/school-teaching-learning/science-or-mathematics-teaching-certificate/",
      "pages": [
        "https://education.ufl.edu/school-teaching-learning/science-or-mathematics-teaching-certificate/"
      ]
    },
    {
      "name": "Social Studies Education",
      "main_url": "https://education.ufl.edu/social-studies-education/",
      "pages": [
        "https://education.ufl.edu/social-studies-education/",
        "https://education.ufl.edu/social-studies-education/admissions/",
        "https://education.ufl.edu/social-studies-education/contact-us/",
        "https://education.ufl.edu/social-studies-education/degrees/doctorate/",
        "https://education.ufl.edu/social-studies-education/degrees/epi-certification/",
        "https://education.ufl.edu/social-studies-education/degrees/mae-online/",
        "https://education.ufl.edu/social-studies-education/degrees/master-of-arts/",
        "https://education.ufl.edu/social-studies-education/degrees/master-of-arts/mae-application-process/",
        "https://education.ufl.edu/social-studies-education/faq/"
      ]
    },
    {
      "name": "Certificate Program in Secondary Teaching Preparation",
      "main_url": "https://education.ufl.edu/school-teaching-learning/secondary-teaching-preparation/",
      "pages": [
        "https://education.ufl.edu/school-teaching-learning/secondary-teaching-preparation/"
      ]
    },
    {
      "name": "Special Education",
      "main_url": "https://education.ufl.edu/special-education/",
      "pages": [
        "https://education.ufl.edu/special-education/",
        "https://education.ufl.edu/special-education/contact-us/",
        "https://education.ufl.edu/special-education/doctoral-programs/",
        "https://education.ufl.edu/special-education/doctoral-programs/concentration",
        "https://education.ufl.edu/special-education/dyslexia-graduate-certificate",
        "https://education.ufl.edu/special-education/graduate-certificate-in-disabilities-in-society/",
        "https://education.ufl.edu/special-education/online-edd/",
        "https://education.ufl.edu/special-education/phd/",
        "https://education.ufl.edu/special-education/program-highlight/",
        "https://education.ufl.edu/special-education/programs/dyslexia/",
        "https://education.ufl.edu/special-education/prospective-students/",
        "https://education.ufl.edu/special-education/prospective-students/doctoral-programs-concentration/",
        "https://education.ufl.edu/special-education/prospective-students/dyslexia-graduate-certificate/",
        "https://education.ufl.edu/special-education/prospective-students/dyslexia-graduate-certificate/application",
        "https://education.ufl.edu/special-education/prospective-students/dyslexia-graduate-certificate/faq",
        "https://education.ufl.edu/special-education/prospective-students/graduate-certificate-in-disabilities-in-society/",
        "https://education.ufl.edu/special-education/prospective-students/on-campus-phd/",
        "https://education.ufl.edu/special-education/prospective-students/on-campus-phd/application/",
        "https://education.ufl.edu/special-education/prospective-students/on-campus-phd/faq/",
        "https://education.ufl.edu/special-education/prospective-students/on-campus-phd/ph-d-program-plan/",
        "https://education.ufl.edu/special-education/prospective-students/online-edd/",
        "https://education.ufl.edu/special-education/prospective-students/online-edd/application/",
        "https://education.ufl.edu/special-education/prospective-students/online-edd/faq/",
        "https://education.ufl.edu/special-education/prospective-students/online-eds/",
        "https://education.ufl.edu/special-education/prospective-students/online-eds/application/",
        "https://education.ufl.edu/special-education/prospective-students/online-eds/faq",
        "https://education.ufl.edu/special-education/prospective-students/online-eds/special-education/prospective-students/online-eds",
        "https://education.ufl.edu/special-education/prospective-students/online-med/",
        "https://education.ufl.edu/special-education/prospective-students/online-med/application",
        "https://education.ufl.edu/special-education/prospective-students/online-med/application/",
        "https://education.ufl.edu/special-education/prospective-students/online-med/faq"
      ]
    },
    {
      "name": "School of Teaching and Learning",
      "main_url": "https://education.ufl.edu/school-teaching-learning/",
      "pages": [
        "https://education.ufl.edu/school-teaching-learning/",
        "http://education.ufl.edu/school-teaching-learning/secondary-teaching-preparation",
        "https://education.ufl.edu/school-teaching-learning/academic-programs/",
        "https://education.ufl.edu/school-teaching-learning/admission-information-for-certificate-programs/",
        "https://education.ufl.edu/school-teaching-learning/admissions/",
        "https://education.ufl.edu/school-teaching-learning/admissions/doctoral-degrees-phd-edd/",
        "https://education.ufl.edu/school-teaching-learning/admissions/master-arts-education-admissions/",
        "https://education.ufl.edu/school-teaching-learning/becoming-a-better-education-professional/",
        "https://education.ufl.edu/school-teaching-learning/becoming-a-teacher/",
        "https://education.ufl.edu/school-teaching-learning/education-specialist-students/",
        "https://education.ufl.edu/school-teaching-learning/faculty-directory/",
        "https://education.ufl.edu/school-teaching-learning/m-ed-students/",
        "https://education.ufl.edu/school-teaching-learning/mae-students/",
        "https://education.ufl.edu/school-teaching-learning/phd-edd-students/",
        "https://education.ufl.edu/school-teaching-learning/pursuing-a-doctoral-degree/",
        "https://education.ufl.edu/school-teaching-learning/recent-faculty-and-program-awards/",
        "https://education.ufl.edu/school-teaching-learning/research/",
        "https://education.ufl.edu/school-teaching-learning/science-or-mathematics-teaching-certificate/",
        "https://education.ufl.edu/school-teaching-learning/secondary-teaching-preparation/",
        "https://education.ufl.edu/school-teaching-learning/selected-funding-opportunities/",
        "https://education.ufl.edu/school-teaching-learning/stl-docseminars/"
      ]
    },
    {
      "name": "School of Human Development and Organizational Studies in Education (HDOSE)",
      "main_url": "https://education.ufl.edu/hdose/",
      "pages": [
        "https://education.ufl.edu/hdose/",
        "https://education.ufl.edu/hdose/graduate-student-funding/",
        "https://education.ufl.edu/hdose/programs/",
        "https://education.ufl.edu/hdose/resources/",
        "https://education.ufl.edu/hdose/staff/"
      ]
    },
    {
      "name": "School of Special Education, School Psychology, and Early Childhood Studies",
      "main_url": "https://education.ufl.edu/sespecs/",
      "pages": [
        "https://education.ufl.edu/sespecs/",
        "https://education.ufl.edu/sespecs/contact-us/",
        "https://education.ufl.edu/sespecs/grants-projects/",
        "https://education.ufl.edu/sespecs/the-team/"
      ]
    },
    {
      "name": "Teacher Leadership for School Improvement",
      "main_url": "https://education.ufl.edu/tlsi/",
      "pages": [
        "https://education.ufl.edu/tlsi/"
      ]
    },
    {
      "name": "UF Teach",
      "main_url": "https://education.ufl.edu/uf-teach/",
      "pages": [
        "https://education.ufl.edu/uf-teach/",
        "https://education.ufl.edu/uf-teach/program-highlights/",
        "https://education.ufl.edu/uf-teach/prospective-students/"
      ]
    },
    {
      "name": "Teachers, Schools, and Society",
      "main_url": "https://education.ufl.edu/curriculum-teaching/",
      "pages": [
        "https://education.ufl.edu/curriculum-teaching/",
        "https://education.ufl.edu/curriculum-teaching/contact-us/",
        "https://education.ufl.edu/curriculum-teaching/edd/",
        "https://education.ufl.edu/curriculum-teaching/edd/admission-requirements",
        "https://education.ufl.edu/curriculum-teaching/edd/faq/",
        "https://education.ufl.edu/curriculum-teaching/edd/key-features",
        "https://education.ufl.edu/curriculum-teaching/edd/program-requirements",
        "https://education.ufl.edu/curriculum-teaching/faculty",
        "https://education.ufl.edu/curriculum-teaching/mae/",
        "https://education.ufl.edu/curriculum-teaching/mae/admission-requirements/",
        "https://education.ufl.edu/curriculum-teaching/mae/faq/",
        "https://education.ufl.edu/curriculum-teaching/mae/program-requirements/",
        "https://education.ufl.edu/curriculum-teaching/on-campus-ph-d/",
        "https://education.ufl.edu/curriculum-teaching/on-campus-ph-d/phd/admission-requirements/",
        "https://education.ufl.edu/curriculum-teaching/on-campus-ph-d/phd/program-study/",
        "https://education.ufl.edu/curriculum-teaching/phd/faq/",
        "https://education.ufl.edu/curriculum-teaching/phd/ph-d-students/",
        "https://education.ufl.edu/curriculum-teaching/student-testimonials/"
      ]
    }
  ]
}
class AccessibilityChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def extract_token_from_html(self, html_content):
        """Extract data-token from HTML response"""
        token_pattern = r'data-token="([^"]+)"'
        match = re.search(token_pattern, html_content)
        if match:
            return match.group(1)
        return None

    def get_loading_page(self, website_url):
        """Step 1: Get the loading page and extract token"""
        encoded_url = quote(website_url, safe='')
        loading_url = f"https://acsbace.com/loading?website={encoded_url}&isPartner=false&embedder=accessibe.com"

        try:
            response = self.session.get(loading_url)
            response.raise_for_status()

            token = self.extract_token_from_html(response.text)
            if not token:
                logger.error(f"Could not extract token for {website_url}")
                return None

            logger.info(f"Token extracted for {website_url}: {token}")
            return token

        except requests.RequestException as e:
            logger.error(f"Error getting loading page for {website_url}: {str(e)}")
            return None

    def start_evaluation(self, website_url, token):
        """Step 2: Start the evaluation process"""
        encoded_url = quote(website_url, safe='')
        evaluate_url = f"https://acsbace.com/evaluate?website={encoded_url}&screenshot=true&token={token}&isPartner=false&embedder=accessibe.com"

        try:
            response = self.session.get(evaluate_url)
            response.raise_for_status()

            logger.info(f"Evaluation started for {website_url}")
            return True

        except requests.RequestException as e:
            logger.error(f"Error starting evaluation for {website_url}: {str(e)}")
            return False

    def get_scan_details(self, token):
        """Step 3: Get detailed scan results"""
        details_url = f"https://acsbace.com/get-scan-details?scanId={token}&embedder=accessibe.com"

        try:
            response = self.session.get(details_url)
            response.raise_for_status()

            scan_data = response.json()
            logger.info(f"Scan details retrieved for token: {token}")
            return scan_data

        except requests.RequestException as e:
            logger.error(f"Error getting scan details for token {token}: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response for token {token}: {str(e)}")
            return None

    def parse_scan_results(self, scan_data):
        """Parse the scan results and extract relevant information"""
        if not scan_data or 'result' not in scan_data:
            return {}

        result = scan_data['result']
        parsed_results = {
            'scanStatus': scan_data.get('scanStatus', ''),
            'verdict': result.get('verdict', ''),
            'score': result.get('score', ''),
            'detectedCMS': result.get('detectedCMS', ''),
            'totalElements': result.get('totalElements', ''),
            'timeToScan': result.get('timeToScan', '')
        }

        # Parse individual report categories
        reports = result.get('reports', {})
        for category, category_data in reports.items():
            if isinstance(category_data, dict):
                parsed_results[f'{category}_verdict'] = category_data.get('verdict', '')
                parsed_results[f'{category}_score'] = category_data.get('score', '')

                # Parse individual tests within each category
                for test_name, test_data in category_data.items():
                    if isinstance(test_data, dict) and 'score' in test_data:
                        parsed_results[f'{category}_{test_name}_score'] = test_data.get('score', '')
                        parsed_results[f'{category}_{test_name}_failures'] = test_data.get('failures', '')
                        parsed_results[f'{category}_{test_name}_successes'] = test_data.get('successes', '')

        return parsed_results

    def check_single_website(self, website_url, progress_callback=None):
        """Check accessibility for a single website"""
        logger.info(f"Starting accessibility check for: {website_url}")

        if progress_callback:
            progress_callback(f"Getting token for {website_url}")

        # Step 1: Get token
        token = self.get_loading_page(website_url)
        if not token:
            return None

        if progress_callback:
            progress_callback(f"Starting evaluation for {website_url}")

        # Step 2: Start evaluation
        if not self.start_evaluation(website_url, token):
            return None

        # Wait for scan to complete
        if progress_callback:
            progress_callback(f"Waiting for scan to complete for {website_url}")
        
        time.sleep(40)

        if progress_callback:
            progress_callback(f"Retrieving results for {website_url}")

        # Step 3: Get scan details
        scan_data = self.get_scan_details(token)
        if not scan_data:
            return None

        # Parse results
        parsed_results = self.parse_scan_results(scan_data)
        parsed_results['website_url'] = website_url
        parsed_results['accessibe_url'] = f"https://accessibe.com/accessscan?website={website_url}"

        return parsed_results

def get_download_link(df, filename="accessibility_results.xlsx"):
    """Generate a download link for the DataFrame as Excel file"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Results')
    
    processed_data = output.getvalue()
    b64 = base64.b64encode(processed_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel file</a>'
    return href

def main():
    st.set_page_config(page_title="Accessibility Checker", page_icon="🔍", layout="wide")
    
    st.title("🔍 Website Accessibility Checker")
    st.markdown("Check the accessibility compliance of UF Education Program websites using AccessiBe's scanner.")
    
    # Create dropdown options
    dropdown_options = ["Run All", "Check One Website"] + [program["name"] for program in UF_PROGRAMS_DATA["uf_education_programs"]]
    
    # Sidebar for controls
    st.sidebar.header("Options")
    selected_option = st.sidebar.selectbox("Select Program to Check:", dropdown_options)
    
    # Display selected option info
    if selected_option == "Run All":
        total_pages = sum(len(program["pages"]) for program in UF_PROGRAMS_DATA["uf_education_programs"])
        st.info(f"Selected: **{selected_option}** - Will check all {total_pages} pages across all programs")
    elif selected_option == "Check One Website":
        st.info("Selected: **Check One Website** - Paste a page link below to check accessibility for a single website.")
        single_url = st.text_input("Paste website URL to check:")
    else:
        selected_program = next(p for p in UF_PROGRAMS_DATA["uf_education_programs"] if p["name"] == selected_option)
        st.info(f"Selected: **{selected_option}** - Will check {len(selected_program['pages'])} pages")
        
        with st.expander("View Pages to be Checked"):
            for page in selected_program["pages"]:
                st.write(f"- {page}")
    
    # Start button
    if st.sidebar.button("🚀 Start Accessibility Check", type="primary"):
        # Collect URLs to process
        urls_to_process = []
        
        if selected_option == "Run All":
            for program in UF_PROGRAMS_DATA["uf_education_programs"]:
                urls_to_process.extend(program["pages"])
        elif selected_option == "Check One Website":
            if single_url:
                urls_to_process = [single_url]
            else:
                st.error("Please paste a website URL to check.")
                return
        else:
            selected_program = next(p for p in UF_PROGRAMS_DATA["uf_education_programs"] if p["name"] == selected_option)
            urls_to_process = selected_program["pages"]
        
        # Initialize checker
        checker = AccessibilityChecker()
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        current_processing = st.empty()
        
        results = []
        total_urls = len(urls_to_process)
        
        # Process each URL
        for i, url in enumerate(urls_to_process):
            # Update progress
            progress_percentage = i / total_urls
            progress_bar.progress(progress_percentage)
            status_text.text(f"Processing {i + 1} of {total_urls} websites...")
            
            def update_current_status(message):
                current_processing.text(message)
            
            # Check website
            result = checker.check_single_website(url, update_current_status)
            
            if result:
                results.append(result)
            else:
                # Add failed entry
                results.append({
                    'website_url': url,
                    'accessibe_url': f"https://accessibe.com/accessscan?website={url}",
                    'scanStatus': 'failed',
                    'verdict': '',
                    'score': ''
                })
            
            # Small delay between requests
            if i < total_urls - 1:
                time.sleep(2)
        
        # Complete progress
        progress_bar.progress(1.0)
        status_text.text("✅ Processing completed!")
        current_processing.text("")
        
        # Create and display results DataFrame
        if results:
            df_results = pd.DataFrame(results)
            
            # Reorder columns to have URL and AccessiBe URL first
            columns_order = ['website_url', 'accessibe_url', 'scanStatus', 'verdict', 'score']
            remaining_columns = [col for col in df_results.columns if col not in columns_order]
            final_columns = columns_order + sorted(remaining_columns)
            
            df_results = df_results.reindex(columns=final_columns)
            
            # Display summary
            st.header("📊 Results Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Pages", len(df_results))
            
            with col2:
                successful_scans = df_results[df_results['scanStatus'] == 'success'].shape[0]
                st.metric("Successful Scans", successful_scans)
            
            with col3:
                failed_scans = df_results[df_results['scanStatus'] != 'success'].shape[0]
                st.metric("Failed Scans", failed_scans)
            
            with col4:
                if successful_scans > 0:
                    avg_score = df_results[df_results['scanStatus'] == 'success']['score'].astype(float).mean()
                    st.metric("Average Score", f"{avg_score:.1f}")
                else:
                    st.metric("Average Score", "N/A")
            
            # Display results table
            st.header("📋 Detailed Results")
            st.dataframe(df_results, use_container_width=True, hide_index=True)
            
            # Download button
            st.header("💾 Download Results")
            st.markdown(get_download_link(df_results), unsafe_allow_html=True)
            
            # Additional analysis
            if successful_scans > 0:
                st.header("📈 Score Distribution")
                
                # Convert scores to numeric for plotting
                numeric_scores = pd.to_numeric(df_results[df_results['scanStatus'] == 'success']['score'], errors='coerce')
                
                if not numeric_scores.empty:
                    st.bar_chart(numeric_scores.value_counts().sort_index())
        
        else:
            st.error("No results were generated. Please check the logs for errors.")

if __name__ == "__main__":
    main()