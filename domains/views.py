from django.shortcuts import render
import requests
from django.conf import settings
from bs4 import BeautifulSoup
from domains.models import DomainAnalysis
import socket
import time
from django.utils import timezone
from django.http import JsonResponse
from .models import Results

def is_non_existent_domain(domain):
    try:
        socket.gethostbyname(domain)
        return False  
    except socket.gaierror:
        return True  

def is_matching_pattern(domain):
    return domain.startswith("164.10")


def analyze2_single_domain(domain):

    http_public_ip = get_public_ip(domain)
    
   
    if http_public_ip == "Non-Existent Domain":
        return {
            'domain': domain,
            'http_status': 'Filtered Out',
            'http_redirect_url': 'N/A',
            'http_final_url': 'N/A',
            'http_public_ip': 'N/A',
            'https_status': 'Filtered Out',
            'https_redirect_url': 'N/A',
            'https_final_url': 'N/A',
            'https_public_ip': 'N/A',
            'remarks': "Non-Existent Domain",
        }
    
    
    if not http_public_ip.startswith("164.100"):
        return {
            'domain': domain,
            'http_status': 'Filtered Out',
            'http_redirect_url': 'N/A',
            'http_final_url': 'N/A',
            'http_public_ip': 'N/A',
            'https_status': 'Filtered Out',
            'https_redirect_url': 'N/A',
            'https_final_url': 'N/A',
            'https_public_ip': 'N/A',
            'remarks': "Public IP does not start with 164.100",
        }


    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        http_status = https_status = None 

        http_public_ip = get_public_ip(domain)
        https_public_ip = get_public_ip(domain)

        http_url = "http://" + domain
        try:
            http_response = requests.get(http_url, allow_redirects=False, timeout=5, headers=headers, verify=False)
            http_status = http_response.status_code
            http_final_url = http_url
            http_redirect_url = None

            if http_status in {301, 302}:
                http_redirect_url = http_response.headers.get('Location')

                http_public_ip = get_public_ip(domain)
                http_final_url = http_redirect_url
        except requests.RequestException:
            http_status = 'Some Error'
            http_final_url = 'N/A'
            http_redirect_url = 'N/A'

        https_url = "https://" + domain
        try:
            https_response = requests.get(https_url, allow_redirects=False, timeout=5, headers=headers, verify=False)
            https_status = https_response.status_code
            https_final_url = https_url
            https_redirect_url = None

            if https_status in {301, 302}:
                https_redirect_url = https_response.headers.get('Location')

                https_public_ip = get_public_ip(domain)
                https_final_url = https_redirect_url
        except requests.RequestException:
            https_status = 'Some Error'
            https_final_url = 'N/A'
            https_redirect_url = 'N/A'

        if http_status in {403, 404, 500}:
            return {
                'domain': domain,
                'http_status': http_status,
                'http_redirect_url': 'N/A',
                'http_final_url': 'N/A',
                'http_public_ip': 'N/A',
                'https_status': 'Filtered Out',
                'https_redirect_url': 'N/A',
                'https_final_url': 'N/A',
                'https_public_ip': 'N/A',
                'remarks': "HTTP Status Code is 403, 404, or 500",
            }

       

        analysis_result = {
            'domain': domain,
            'http_status': http_status,
            'http_redirect_url': http_redirect_url,
            'http_final_url': http_final_url,
            'http_public_ip': http_public_ip,
            'https_status': https_status,
            'https_redirect_url': https_redirect_url,
            'https_final_url': https_final_url,
            'https_public_ip': https_public_ip,
            'remarks': "Success",
        }
        
        obj1 = Results(
            domain=domain,
            Public_ip=http_public_ip,
            status_code_if_redirected=http_redirect_url,
            http_status=http_status,
            https_redirect_url=https_redirect_url,
            https_status=https_status,
        )
        obj1.save()
        
        print(analysis_result)
        return analysis_result

        return JsonResponse(analysis_result)
    except requests.RequestException:
        return {
            'domain': domain,
            'http_status': 'Some Error',
            'http_redirect_url': 'N/A',
            'http_final_url': 'N/A',
            'http_public_ip': 'N/A',
            'https_status': 'Some Error',
            'https_redirect_url': 'N/A',
            'https_final_url': 'N/A',
            'https_public_ip': 'N/A',
            'remarks': "Error fetching data",
        }

def phase2_domain(request):
    
    if 'analysis_results' in request.session:
        
        analysis_results = request.session['analysis_results']

       
        filtered_status_codes = [403, 404, 500]
        filtered_results = []

        for result in analysis_results:
            http_public_ip = result.get('http_public_ip', '')
            https_public_ip = result.get('https_public_ip', '')

            
            if http_public_ip.startswith("164.10") :
               
                if result['http_status'] not in filtered_status_codes and result['https_status'] not in filtered_status_codes:
                    filtered_results.append(result)

        return render(request, 'phase2.html', {'filtered_results': filtered_results})



    return render(request, 'upload.html')

def get_public_ip(domain ):
    try:
        ip_address = socket.gethostbyname(domain)
        return (ip_address)
    except:
        return str("Non-Existent Domain")



def analyze_single_domain(domain):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        
        http_public_ip = get_public_ip(domain)
        https_public_ip = get_public_ip(domain)

       
        http_url = "http://" + domain
        try:
            http_response = requests.get(http_url, allow_redirects=False, timeout=5, headers=headers, verify=False)
            http_status = http_response.status_code
            http_final_url = http_url
            http_redirect_url = None
            
            if http_status in {301, 302}:
                http_redirect_url = http_response.headers.get('Location')
               
                http_public_ip = get_public_ip(domain)
                http_final_url = http_redirect_url
        except requests.RequestException:
            http_status = 'Some Error'
            http_final_url = 'N/A'
            http_redirect_url = 'N/A'
        
       
        https_url = "https://" + domain
        try:
            https_response = requests.get(https_url, allow_redirects=False, timeout=5, headers=headers, verify=False)
            https_status = https_response.status_code
            https_final_url = https_url
            https_redirect_url = None
            
            if https_status in {301, 302}:
                https_redirect_url = https_response.headers.get('Location')
               
                https_public_ip = get_public_ip(domain)
                https_final_url = https_redirect_url
        except requests.RequestException:
            https_status = 'Some Error'
            https_final_url = 'N/A'
            https_redirect_url = 'N/A'
        
        analysis_result = {
            'domain': domain,
            'http_status': http_status,
            'http_redirect_url': http_redirect_url, 
            'http_final_url': http_final_url,
            'http_public_ip': http_public_ip, 
            'https_status': https_status,
            'https_redirect_url': https_redirect_url, 
            'https_final_url': https_final_url,
            'https_public_ip': https_public_ip,  
            'remarks': "Success",
        }
        obj1 = Results(
            domain=domain,
            Public_ip= http_public_ip,
            status_code_if_redirected= http_redirect_url,
            http_status = http_status,
            https_redirect_url= https_redirect_url,
            https_status= https_status)
            # timestamp=timezone  )
            # http_final_url=http_final_url
            
            
            
            # https_final_url= https_final_url,
            # https_public_ip= https_public_ip,  
            # remarks= "Success")
        obj1.save() 
    
        print(analysis_result)
        return analysis_result

    except requests.RequestException:
       
        return {
            'domain': domain,
            'http_status': 'Some Error',
            'http_redirect_url': 'N/A',
            'http_final_url': 'N/A',
            'http_public_ip': 'N/A',
            'https_status': 'Some Error',
            'https_redirect_url': 'N/A',
            'https_final_url': 'N/A',
            'https_public_ip': 'N/A',
            'remarks': "Error fetching data",
        }

def process_analysis_result(analysis_result):
    
    http_status = analysis_result['http_status']
    https_status = analysis_result['https_status']
    
    if http_status >= 400 and https_status >= 400:
        analysis_result['remarks'] = "Site is not working"
    elif http_status >= 400 or https_status >= 400:
        analysis_result['remarks'] = "Server gives 40X error"
    elif http_status >= 500 or https_status >= 500:
        analysis_result['remarks'] = "Server gives 50X error"
    elif http_status == 200 and https_status == 200:
        http_title = get_title("http://" + analysis_result['domain'])
        https_title = get_title("https://" + analysis_result['domain'])
        
        if http_title and https_title and http_title != https_title:
            analysis_result['remarks'] = "Titles for http and https differ"
        else:
            analysis_result['remarks'] = "Site is up"
    elif http_status in {301, 302} and https_status == 200:
        analysis_result['remarks'] = "Ideal scenario for redirection"
    else:
        analysis_result['remarks'] = "Site status not determined"

def get_title(url):
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string.strip()
            return title
    except requests.RequestException:
        pass
    
    return None

def analyze_statuses(http_status, https_status):
    if http_status == 200 and https_status == 200:
        return "Site is working on both HTTP and HTTPS."
    elif http_status >= 400 or https_status >= 400:
        return "Site is not working."
    elif http_status >= 300 and http_status < 400:
        return "Site is redirecting on HTTP."
    elif https_status >= 300 and https_status < 400:
        return "Site is redirecting on HTTPS."
    elif http_status >= 500 or https_status >= 500:
        return "Server error on ."


def analyze_domain(request):
    if request.method == 'POST' and request.FILES['domain_list']:
        
        uploaded_file = request.FILES['domain_list']
       
        domain_list = uploaded_file.read().decode('utf-8').split('\r\n')
        analysis_results = []

        for domain in domain_list:
            domain = domain.strip()
            if domain:
                analysis_result = analyze_single_domain(domain)
                analysis_results.append(analysis_result)

        
        request.session['analysis_results'] = analysis_results
        request.session.save()

        return render(request, 'result.html', {'results': analysis_results})

    return render(request, 'upload.html')
    
# def analyze_domain(request):
#     if request.method == 'POST' and request.FILES['domain_list']:
#         domain_list = request.FILES['domain_list'].read().decode('utf-8').split('\n')
#         analysis_results = []

#         # Fetch the public IP address of your server
#         public_ip = get_public_ip(domain)

#         for domain in domain_list:
#             domain = domain.strip()
#             if domain:
#                 analysis_result = analyze_single_domain(domain)
#                 analysis_results.append(analysis_result)

#         # obj1 = Results(
#         # domain=analysis_result['domain'],
#         # http_status = analysis_result['http_status'],
#         # http_redirect_url= analysis_result['http_redirect_url'],
#         # http_final_url=analysis_result['http_final_url'],
#         # http_public_ip= analysis_result['http_public_ip'],  
#         # https_status= analysis_result['https_status'],
#         # https_redirect_url= analysis_result['https_redirect_url'],
#         # https_final_url= analysis_result['https_final_url'],
#         # https_public_ip= analysis_result['https_public_ip'], 
#         # remarks= "Success")
#         # obj1.save()
#         print(analysis_results)
#         return render(request, 'result.html', {'results': analysis_results, 'public_ip': public_ip})
    
    
#         # obj1 = Results(
#         #         domain=analysis_result[domain],
#         #         http_status = analysis_result[http_status],
#         #         http_redirect_url= analysis_result[http_redirect_url],
#         #         http_final_url=analysis_result[http_final_url],
#         #         http_public_ip= analysis_result[http_public_ip],  
#         #         https_status= analysis_result[https_status],
#         #         https_redirect_url= analysis_result[https_redirect_url],
#         #         https_final_url= analysis_result[https_final_url],
#         #         https_public_ip= analysis_result[https_public_ip], 
#         #         remarks= "Success")
#         # obj1.save()     
#     return render(request, 'upload.html')

def analyze_multiple_domains(request):
    domain = [
'hyd.sms.gov.in',
'hydrep.sms.gov.in',
'ncpcr.gov.in',
'ndmis.mha.gov.in',
'gepg.nic.in',
    ]

    analysis_results = []

    for domain in Domains1:
        analysis_result = analyze_single_domain(domain)
        analysis_results.append(analysis_result)
     
        

    DomainAnalysis.objects.bulk_create([
        DomainAnalysis(**result) for result in analysis_results
    ])
    


    return render(request, 'result.html', {'results': analysis_results})

def update_domain_ips(request):

    Domains1 = [
        'hyd.sms.gov.in',
        'hydrep.sms.gov.in',
        'ncpcr.gov.in',
        'ndmis.mha.gov.in',
        'gepg.nic.in',
    ]
    
    try:
        # Get the public IP address of your server
        public_ip = get_public_ip(domain)
    except Exception as e:
        public_ip = 'N/A'

    analysis_results = []

    for domain in Domains1:
        try:
            # Check if the domain already exists in the database
            existing_domain = DomainAnalysis.objects.filter(domain=domain).first()
            if existing_domain:
                existing_domain.public_ip = public_ip
                existing_domain.save()
            else:
                DomainAnalysis.objects.create(domain=domain, public_ip=public_ip, http_status=0, https_status=0, remarks="N/A")

            # Analyze the domain and fetch IP
            analysis_result = analyze_single_domain(domain, public_ip)
            analysis_results.append(analysis_result)

        except Exception as e:
            print(f"Error updating IP for domain {domain}: {str(e)}")
        

    DomainAnalysis.objects.bulk_create([
        DomainAnalysis(**result) for result in analysis_results
    ])
    
    return render(request, 'result.html', {'message': 'Domain IPs updated successfully'})
     
    
    # obj1 = Results(
    #         domain=analysis_result[domain],
    #         http_status = analysis_result[http_status],
    #         http_redirect_url= analysis_result[http_redirect_url],
    #         http_final_url=analysis_result[http_final_url],
    #         http_public_ip= analysis_result[http_public_ip],  
    #         https_status= analysis_result[https_status],
    #         https_redirect_url= analysis_result[https_redirect_url],
    #         https_final_url= analysis_result[https_final_url],
    #         https_public_ip= analysis_result[https_public_ip], 
    #         remarks= "Success")
    # obj1.save() 




