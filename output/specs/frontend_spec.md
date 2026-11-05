## `frontend_spec.md`

```markdown
# frontend_spec.md

## Estado

**Implementación de integración bloqueada por falta del contrato aprobado de login.** El historial solo aporta el nombre de la feature y criterios derivados de su título; no incluye la ruta, el método, el esquema de entrada, la respuesta de éxito ni el formato de errores del endpoint.

Los archivos de código incluidos abajo son un **armazón de integración**, no una implementación lista para producción: no inventan campos ni una URL, y requieren que la aplicación anfitriona proporcione el formulario y la configuración del endpoint según el contrato vigente.

## Recorrido y campos

El recorrido previsto es: completar el formulario existente, enviarlo, mostrar progreso, y dejar que la aplicación anfitriona gestione el resultado de éxito conforme al contrato aprobado. El componente de ejemplo recibe el `FormGroup` y una función que construye la solicitud; no define campos ni transforma el payload.

| Campo | Validación visible | Estado |
|---|---|---|
| Campos del login | No se pueden especificar nombres, tipos ni reglas sin el esquema aprobado. El contenedor marca los controles del `FormGroup` como tocados y presenta un aviso genérico si el formulario es inválido. | **SUPUESTO PENDIENTE:** Backend y Arquitectura/API deben proporcionar el esquema y las validaciones. |
| Mensajes específicos por campo | No se implementan: no se conocen los campos ni sus restricciones. | **SUPUESTO PENDIENTE:** Frontend y Backend deben acordar los mensajes una vez disponible el esquema. |

El navegador puede apoyar la experiencia de validación, pero la validación y autorización definitivas corresponden al servidor.

## Acciones y estados

- **Editar:** los campos se proyectan desde la aplicación anfitriona; sus etiquetas, ayudas y errores específicos deben definirse conforme al contrato.
- **Enviar:** el componente comprueba el `FormGroup`, marca sus controles como tocados si es inválido y evita envíos duplicados mientras carga.
- **Carga:** se deshabilita el botón y se anuncia el progreso.
- **Inicial/sin solicitud:** se muestra una indicación para completar el formulario.
- **Éxito:** se anuncia que la solicitud se completó y se emite la respuesta sin mostrarla. La aplicación anfitriona debe procesarla según el contrato.
- **Error:** se muestra un mensaje genérico, sin mostrar el cuerpo técnico de la respuesta.
- **Vacío:** no aplica un estado de lista vacía a este recorrido de login.
- **Error de campo frente a error de API:** el armazón cubre el resumen genérico del formulario y el mensaje de API. Los errores específicos por campo quedan pendientes del esquema.

## Mapeo genérico de estados HTTP

No se proporcionó el catálogo de errores del endpoint. Los mensajes de abajo son una **capa de UX genérica basada en los estados mencionados en la solicitud**, no una afirmación del significado contractual de cada error. No se leen ni se muestran mensajes, códigos, stack traces ni otros detalles del cuerpo devuelto por el servidor.

| Estado HTTP | Mensaje genérico mostrado |
|---|---|
| 400 | No se pudo procesar la solicitud. Revisa los datos e inténtalo de nuevo. |
| 401 | No se pudo iniciar sesión. Verifica los datos e inténtalo de nuevo. |
| 403 | No tienes autorización para realizar esta acción. |
| 404 | No se encontró el recurso solicitado. |
| 409 | No se pudo completar la solicitud por un conflicto. Inténtalo de nuevo. |
| 5xx | Ocurrió un problema temporal. Inténtalo más tarde. |
| Sin respuesta de red u otro estado | No pudimos completar la solicitud. Inténtalo de nuevo más tarde. |

**Pendiente:** Backend y Arquitectura/API deben confirmar los estados y mensajes compatibles con el contrato. El mapeo debe ajustarse si el contrato establece otra semántica.

## Criterios de aceptación y evidencia

Los siguientes criterios son **derivados del título**, no la lista oficial del Issue:

| Criterio derivado | Archivo y elemento | Comprobación propuesta |
|---|---|---|
| La interfaz no muestra ni vuelve a imprimir los valores de entrada o una respuesta cruda. | `login-submit.component.html`: la plantilla no interpola el payload ni la respuesta. | Con una respuesta de prueba que contenga un valor centinela, comprobar que el texto del componente no lo muestra. La salida de éxito permite al host procesar la respuesta y no debe usarse para mostrarla indiscriminadamente. |
| No se muestran detalles técnicos de errores. | `login-api.service.ts`: `getLoginErrorMessage`; `login-submit.component.html`: región `role="alert"`. | Simular los estados contemplados y verificar que se muestra solo el mensaje genérico; comprobar que no aparecen el cuerpo, stack trace ni mensajes técnicos del error. |
| El éxito conserva el payload que requiera el contrato público. | `login-api.service.ts`: tipo de respuesta `LoginResponse`; `login-submit.component.ts`: evento `loginSucceeded`. | Cuando Backend entregue el contrato, probar que el host consume solo los campos aprobados. No se puede verificar el contrato actual con la información recibida. |
| Se contemplan carga y errores sin duplicar envíos. | `login-submit.component.ts` y `login-submit.component.html`: `loading`, botón deshabilitado y feedback. | Con una respuesta HTTP demorada, comprobar el progreso y que el botón no permite otro envío; finalizar con éxito y con error. |
| La validación del cliente no sustituye al servidor. | `login-submit.component.ts`: formulario inválido impide el envío en cliente; el servicio sigue dejando la validación final al API. | Enviar una solicitud inválida de formulario y verificar que no se llama al servicio. Confirmar por separado que Backend valida la solicitud. |
| Los controles son accesibles. | `login-submit.component.html`: formulario, feedback y estado con regiones anunciables; `login-submit.component.ts`: foco al resumen. Los campos se proyectan desde el host. | Teclado: recorrer campos y botón, enviar con Enter, provocar error y verificar foco/anuncio. Revisar etiquetas y errores de cada campo en el host. |

## Accesibilidad

- El host debe proporcionar etiquetas asociadas a cada control y errores específicos vinculados al campo según el esquema aprobado.
- La plantilla usa `role="alert"` para feedback y `role="status"`/`aria-live` para progreso y éxito.
- Al encontrar un formulario inválido o un error de API, el componente mueve el foco al mensaje de feedback.
- El botón de envío es operable por teclado y queda deshabilitado durante la carga.
- El CSS evita imponer colores de texto o fondo; el host debe asegurar contraste WCAG suficiente para su tema y verificar el indicador de foco en la aplicación.

## Supuestos pendientes

1. **Arquitectura/API y Backend:** proporcionar el endpoint y método existentes, el esquema de solicitud, las validaciones, el payload de éxito y el catálogo/envelope de errores.
2. **Frontend:** integrar el formulario aprobado en el contenido proyectado, asociar sus etiquetas y mensajes de error, y proporcionar `buildRequest`.
3. **Aplicación anfitriona:** proporcionar `LOGIN_API_ENDPOINT` con la URL contractual y procesar `loginSucceeded` sin mostrar la respuesta cruda.
4. No se cambia ni filtra arbitrariamente la respuesta: sin conocer el contrato, hacerlo podría eliminar datos públicos requeridos para completar el login. La eliminación de eco y detalles internos debe garantizarla principalmente el servidor.

## Verificación

**NO EJECUTADO.** No se proporcionó el proyecto Angular y no se ejecutaron pruebas ni compilación.

Cuando el código esté integrado en el proyecto, ejecutar, según la configuración disponible:

```bash
ng test
ng build
```

Pruebas sugeridas con Jasmine/Karma y `HttpTestingController`: solicitud enviada al endpoint configurado; respuesta con valor centinela no mostrada por el componente; mensajes genéricos para los estados previstos; formulario inválido sin petición; estado de carga y prevención de doble envío; foco y anuncios accesibles.
```

El código siguiente es deliberadamente genérico. **No define campos ni una URL** y requiere integración con el formulario y la configuración reales antes de usarse.

```typescript
// login-api.model.ts

/**
 * El contrato de login no fue proporcionado.
 * Se usan tipos opacos para no inventar campos ni alterar el payload.
 */
export type LoginRequest = unknown;
export type LoginResponse = unknown;
```

```typescript
// login-api.service.ts

import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Inject, Injectable, InjectionToken } from '@angular/core';
import { Observable } from 'rxjs';
import { LoginRequest, LoginResponse } from './login-api.model';

/**
 * La aplicación debe proporcionar el endpoint ya aprobado.
 * No se establece aquí una ruta por falta del contrato.
 */
export const LOGIN_API_ENDPOINT = new InjectionToken<string>(
  'LOGIN_API_ENDPOINT',
);

@Injectable({ providedIn: 'root' })
export class LoginApiService {
  constructor(
    private readonly http: HttpClient,
    @Inject(LOGIN_API_ENDPOINT) private readonly endpoint: string,
  ) {}

  login(request: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(this.endpoint, request);
  }
}

/**
 * Mensajes genéricos de UX. No usa el cuerpo del error ni afirma
 * que estos estados sean el catálogo contractual del endpoint.
 */
export function getLoginErrorMessage(error: unknown): string {
  if (!(error instanceof HttpErrorResponse)) {
    return 'No pudimos completar la solicitud. Inténtalo de nuevo más tarde.';
  }

  switch (error.status) {
    case 0:
      return 'No pudimos conectar con el servicio. Inténtalo de nuevo más tarde.';
    case 400:
      return 'No se pudo procesar la solicitud. Revisa los datos e inténtalo de nuevo.';
    case 401:
      return 'No se pudo iniciar sesión. Verifica los datos e inténtalo de nuevo.';
    case 403:
      return 'No tienes autorización para realizar esta acción.';
    case 404:
      return 'No se encontró el recurso solicitado.';
    case 409:
      return 'No se pudo completar la solicitud por un conflicto. Inténtalo de nuevo.';
    default:
      if (error.status >= 500 && error.status <= 599) {
        return 'Ocurrió un problema temporal. Inténtalo más tarde.';
      }

      return 'No pudimos completar la solicitud. Inténtalo de nuevo más tarde.';
  }
}
```

```typescript
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
```

```html
<!-- login-submit.component.html -->

<section aria-labelledby="login-heading">
  <h1 id="login-heading">Iniciar sesión</h1>

  <form [formGroup]="form" (ngSubmit)="submit()" novalidate>
    <!--
      El host debe proyectar aquí los controles del contrato aprobado,
      con etiquetas asociadas y mensajes de validación por campo.
    -->
    <ng-content select="[loginFields]"></ng-content>

    <div
      #feedback
      class="feedback"
      role="alert"
      aria-live="assertive"
      tabindex="-1"
    >
      {{ feedbackMessage }}
    </div>

    <p *ngIf="loading" role="status" aria-live="polite">
      Enviando solicitud…
    </p>

    <p *ngIf="statusMessage && !loading" role="status" aria-live="polite">
      {{ statusMessage }}
    </p>

    <p *ngIf="!loading && !feedbackMessage && !statusMessage">
      Completa el formulario para continuar.
    </p>

    <button type="submit" [disabled]="loading">
      {{ loading ? 'Enviando…' : 'Iniciar sesión' }}
    </button>
  </form>
</section>
```

```css
/* login-submit.component.css */

:host {
  display: block;
}

.feedback:empty {
  display: none;
}

button:focus-visible {
  outline: 3px solid currentColor;
  outline-offset: 3px;
}
```