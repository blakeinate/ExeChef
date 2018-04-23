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
import { User, Settings } from '../models';


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
    let access_token = this.jwtService.getToken();
    let refresh_token = this.jwtService.getRefreshToken();

    if(access_token){
      this.apiService.postRefresh('/Refresh').subscribe(
        data =>{
           access_token = data.access_token;
           this.apiService.get('/User')
           .subscribe(
             data => {
               data.user.access_token = access_token;
               data.user.refresh_token = refresh_token;
               this.setAuth(data.user)
             },
             err => {
                this.purgeAuth()
             }
           );
        },
        err => {
            this.purgeAuth();
            this.router.navigateByUrl('/login');

        }
      )
    } else{
      this.purgeAuth();
    }
  }

  refresh(){
    let access_token = this.jwtService.getToken();
    let refresh_token = this.jwtService.getRefreshToken();
    if(access_token){

       this.apiService.postRefresh('/Refresh').subscribe(
        data =>{
           access_token = data.access_token;
           this.jwtService.saveTokens(access_token,refresh_token);
        },
        err => {
            this.purgeAuth();
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
    let route = (type === 'login') ? '/Login' : '/User';
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


  update(newSettings:Settings):Observable<User>{
    //When updating user service there is a weird bug that nullifys following if you favorite and vise versa when you just put 1 of the settings
    //as a temp fix I grab the last favorite value or the last following value and send them combined with the new verison of the other.
    //this might be a backend related issue and will need to further investigate
    let settings;
    if(newSettings.following || newSettings.favorites){
      settings = this.getCurrentUser();
      Object.assign(settings,newSettings);
      Object.assign(newSettings,{following:settings.following,favorites: settings.favorites})
    }

    console.log("what im sending",newSettings);
    return this.apiService.put('/User',newSettings)
    .map(
      data =>{
        console.log("update send back",data);
        this.currentUserSubject.next(data.user);
        return data.user;
      });
  }

}
