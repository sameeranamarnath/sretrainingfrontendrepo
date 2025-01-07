import { Component } from '@angular/core';
import axios from 'axios';

@Component({
  selector: 'app-employee-dashboard',
  templateUrl: './employee-dashboard.component.html',
  styleUrls: ['./employee-dashboard.component.css']
})
export class EmployeeDashboardComponent {
  employeeName: string = '';
  password: string = '';
  isAuthenticated: boolean = false;
  performanceScore: string = '';
  benefitPlans: string = '';
  performanceReview: string = '';

  onLogin() {
    const loginData = { employeeName: this.employeeName, password: this.password };

    axios.get('https://crispy-space-zebra-5j5g46gvvr3vw4q-8100.app.github.dev/employees/authenticateEmployee')
      .then(response => {
        this.isAuthenticated = true;
        console.log(response.data);
        this.fetchEmployeeData();
         
        if (response.data.success) {
          this.isAuthenticated = true;
          // Handle successful authentication, e.g., load dashboard data
        } else {
         // alert('Authentication failed. Please check your credentials.');
        }
      })
      .catch(error => {
        this.isAuthenticated = true;
        //this.fetchEmployeeData();
        
       
        console.error('There was an error during authentication:', error);
        //alert('An error occurred. Please try again later.');
      });
  }

  fetchEmployeeData() {
    axios.get('https://crispy-space-zebra-5j5g46gvvr3vw4q-8100.app.github.dev/employees/getEmployeeData')
      .then(response => {
        const data = response.data;
        console.log("employee data:"+ JSON.stringify(data));
        this.performanceScore = data.QPS;
        this.benefitPlans = data.Benefits;
        this.performanceReview = data.PerformanceReviewScore;
      })
      .catch(error => {
        console.error('Error fetching employee data', error);
      });
  }
}

