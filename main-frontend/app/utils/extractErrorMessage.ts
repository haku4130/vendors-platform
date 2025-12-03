import type { HttpValidationError } from '~/generated/api';

export function extractErrorMessage(
    error: HttpValidationError,
    dflt: string = 'Something went wrong'
): string {
    let detail: string;

    if (typeof error.detail === 'string') {
        detail = error.detail;
    } else if (Array.isArray(error.detail)) {
        detail = error.detail[0]?.msg ?? dflt;
    } else {
        detail = dflt;
    }

    return detail;
}
