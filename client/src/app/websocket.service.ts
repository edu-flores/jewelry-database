import { Injectable } from '@angular/core';
import { io } from 'socket.io-client';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  private socket = io('http://localhost:5002');

  // Emit an update to the GPS API service
  sendUpdate() {
    this.socket.emit('update');
  }

  // Receive updates from the GPS API service
  getUpdates() {
    let observable = new Observable<any>((observer) => {
      this.socket.on('updated', (data) => {
        observer.next(data);
      });
    });
    return observable;
  }
}
