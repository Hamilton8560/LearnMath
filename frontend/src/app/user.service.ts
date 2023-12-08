import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private userEmailSource = new BehaviorSubject<string | null>(localStorage.getItem('userEmail'));
  private difficultySource = new BehaviorSubject<string | null>(localStorage.getItem('difficulty'));
  difficulty = this.difficultySource.asObservable();
  userEmail = this.userEmailSource.asObservable();

  constructor(private http: HttpClient) {}

  setUserEmail(email: string) {
    localStorage.setItem('userEmail', email); 
    this.userEmailSource.next(email);
  }
  setUserDifficulty(difficulty){
    localStorage.setItem('difficulty', difficulty)
    this.difficultySource.next(difficulty);
  }
  getUserdifficulty(email){
    const url = 'http://127.0.0.1:3000/api/users/info';
    const params = new HttpParams().set('email', email);
    return this.http.get(url, {params})
  }
  patchDifficulty(email: string, difficulty: number): Observable<any> {
    const apiUrl = 'http://127.0.0.1:3000/api/users/info'
      const params = new HttpParams().set('email', email).set('difficulty', difficulty.toString());
      return this.http.patch(apiUrl, {}, { params });
    }

  checkUsername(email: string) {
    const url = 'http://127.0.0.1:3000/api/users/exists';
    const params = new HttpParams().set('email', email);
    return this.http.get(url, {params});
  }
 
  getUser(email){
    const url = 'http://127.0.0.1:3000//api/users/info';
    const params= new HttpParams().set('email', email);
    return this.http.get(url,{params});


  }
  createUser(userInfo: any) {
    return this.http.post('http://127.0.0.1:3000/api/users/create', userInfo);
  }

  authUser(loginInfo: any) {
    return this.http.post('http://127.0.0.1:3000/api/users/auth', loginInfo)
  }
}
