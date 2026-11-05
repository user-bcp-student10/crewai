// login-submit.component.ts

import {
  Component,
  ElementRef,
  EventEmitter,
  Input,
  Output,
  ViewChild,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';
import { LoginApiService, getLoginErrorMessage } from './login-api.service';
import { LoginRequest, LoginResponse } from './login-api.model';

@Component({
  selector: 'app-login-submit',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login-submit.component.html',
  styleUrls: ['./login-submit.component.css'],
})
export class LoginSubmitComponent {
  /**
   * El host debe construir este formulario con los controles y validaciones
   * definidos por el contrato aprobado.
   */
  @Input() form!: FormGroup;

  /**
   * El host debe construir el payload de acuerdo con el contrato aprobado.
   * Se espera una función flecha si necesita acceder al contexto del host.
   */
  @Input() buildRequest!: () => LoginRequest;

  /**
   * La respuesta se entrega al host para que gestione solo los campos
   * públicos establecidos por el contrato. Este componente no la muestra.
   */
  @Output() readonly loginSucceeded = new EventEmitter<LoginResponse>();

  @ViewChild('feedback')
  private feedback?: ElementRef<HTMLElement>;

  loading = false;
  feedbackMessage = '';
  statusMessage = '';

  constructor(private readonly loginApi: LoginApiService) {}

  submit(): void {
    if (this.loading) {
      return;
    }

    if (!this.form || !this.buildRequest) {
      this.showError('No se pudo completar la solicitud. Inténtalo de nuevo más tarde.');
      return;
    }

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      this.statusMessage = '';
      this.showError('Revisa los campos del formulario e inténtalo de nuevo.');
      return;
    }

    let request: LoginRequest;

    try {
      request = this.buildRequest();
    } catch {
      this.showError('No se pudo completar la solicitud. Inténtalo de nuevo más tarde.');
      return;
    }

    this.feedbackMessage = '';
    this.statusMessage = '';
    this.loading = true;

    this.loginApi.login(request).subscribe({
      next: (response) => {
        this.loading = false;
        this.statusMessage = 'La solicitud se completó.';
        this.loginSucceeded.emit(response);
      },
      error: (error: unknown) => {
        this.loading = false;
        this.showError(getLoginErrorMessage(error));
      },
    });
  }

  private showError(message: string): void {
    this.feedbackMessage = message;

    // Permite que Angular actualice la región antes de mover el foco.
    setTimeout(() => this.feedback?.nativeElement.focus());
  }
}