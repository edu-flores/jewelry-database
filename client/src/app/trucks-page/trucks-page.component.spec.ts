import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TrucksPageComponent } from './trucks-page.component';

describe('TrucksPageComponent', () => {
  let component: TrucksPageComponent;
  let fixture: ComponentFixture<TrucksPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TrucksPageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TrucksPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
