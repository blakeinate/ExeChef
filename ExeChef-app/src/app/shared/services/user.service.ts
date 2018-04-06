import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import { Observable } from 'rxjs/Rx';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { ReplaySubject } from 'rxjs/ReplaySubject';
import { Router} from '@angular/router';

import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { ApiService } from './api.service';
import { JwtService } from './jwt.service';
import { User } from '../models';


@Injectable()
export class UserService {
    refresh_token: String
  private currentUserSubject = new BehaviorSubject<User>(new User());
  //distinctUntilChanged only emmits a user when the user is different from the last
  public currentUser = this.currentUserSubject.asObservable().distinctUntilChanged();

  private isAuthenticatedSubject = new ReplaySubject<boolean>(1);
  public isAuthenticated = this.isAuthenticatedSubject.asObservable();

  constructor (
    private apiService: ApiService,
    private http: Http,
    private jwtService: JwtService,
    private router: Router
  ) {}


  populate(){
    //need to set the accsess token as the refresh then when I call refresh
    //get the accsess token and set it as acsess token and keep the refresh token the same
    let access_token = this.jwtService.getToken();
    let refresh_token = this.jwtService.getRefreshToken();
    //set the accsess token to the refresh one when calling refresh route so it can pass in the header for the api call.
    // when we call jwtService.getToken() now we should get the refresh not the accsess
    this.jwtService.saveToken(refresh_token);
    if(access_token){
      this.apiService.post('/Refresh').subscribe(
        data =>{
           access_token = data.access_token;
           //reset back to origanal form so the user route can set access token as header
           this.jwtService.saveToken(access_token);
           this.apiService.get('/User')
           .subscribe(
             data => {
               data.user.access_token = access_token;
               data.user.refresh_token = refresh_token;
               this.setAuth(data.user)
             },
             err => this.purgeAuth()
           );
        },
        err => {
            this.router.navigateByUrl('/login');
        }
      )
    } else{
      this.purgeAuth();
    }
  }

  setAuth(user: User) {
    //save tokens
    this.jwtService.saveTokens(user.access_token,user.refresh_token);
    // Set current user data into observable
    this.currentUserSubject.next(user);
    // Set isAuthenticated to true
    this.isAuthenticatedSubject.next(true);
  }

  purgeAuth(){
    //destroy token, set to empty user object and set auth to false
    this.jwtService.destoryToken();
    this.currentUserSubject.next(new User());
    this.isAuthenticatedSubject.next(false);
  }

  attemptAuth(type, credentials): Observable<User> {
    let route = (type === 'login') ? '/Login' : '/CreateAccount';
    return this.apiService.post(route, credentials)
    .map(
      data => {
        this.setAuth(data.user);
        return data;
      }
    );
  }

  getCurrentUser(): User {
    return this.currentUserSubject.value;
  }

  update(user:User):Observable<User>{
    return this.apiService.put('/user',{user})
    .map(
      data =>{
        this.currentUserSubject.next(data.user);
        return data.user;
      });
  }

}
