<template>
  <AuthFormContainer class="max-w-sm">
    <div v-if="!tokenError" class="text-start space-y-1">
      <h2 class="text-xl font-semibold">Reset Password</h2>
      <p class="text-sm mb-6 text-gray-600">Enter your new password below.</p>
    </div>

    <div v-if="tokenError" class="space-y-4">
      <div class="flex justify-center mb-4">
        <UIcon name="i-lucide-alert-circle" class="text-6xl text-error" />
      </div>
      <h3 class="text-lg font-semibold text-center">Invalid or Expired Link</h3>
      <p class="text-center text-gray-600">
        This password reset link is invalid or has expired. Please request a new
        one.
      </p>
      <UButton
        variant="solid"
        color="warning"
        size="lg"
        class="w-full justify-center"
        to="/forgot-password"
      >
        Request New Link
      </UButton>
    </div>

    <UForm
      v-else-if="!passwordReset"
      :schema="schema"
      :state="state"
      class="space-y-4"
      @submit="onSubmit"
    >
      <UFormField label="New Password" name="password">
        <UInput
          v-model="state.password"
          leading-icon="i-lucide-lock"
          class="w-full"
          :type="showPassword ? 'text' : 'password'"
          :ui="{ trailing: 'pe-1' }"
          :disabled="isSubmitting"
        >
          <template #trailing>
            <UButton
              color="neutral"
              variant="link"
              size="sm"
              :icon="showPassword ? 'i-lucide-eye-off' : 'i-lucide-eye'"
              :aria-label="showPassword ? 'Hide password' : 'Show password'"
              :aria-pressed="showPassword"
              @click="showPassword = !showPassword"
            />
          </template>
        </UInput>
        <template #help>
          <span class="text-xs text-gray-600">
            Password must be at least 8 characters long
          </span>
        </template>
      </UFormField>

      <UFormField label="Confirm Password" name="confirmPassword">
        <UInput
          v-model="state.confirmPassword"
          leading-icon="i-lucide-lock"
          class="w-full"
          :type="showConfirmPassword ? 'text' : 'password'"
          :ui="{ trailing: 'pe-1' }"
          :disabled="isSubmitting"
        >
          <template #trailing>
            <UButton
              color="neutral"
              variant="link"
              size="sm"
              :icon="showConfirmPassword ? 'i-lucide-eye-off' : 'i-lucide-eye'"
              :aria-label="
                showConfirmPassword ? 'Hide password' : 'Show password'
              "
              :aria-pressed="showConfirmPassword"
              @click="showConfirmPassword = !showConfirmPassword"
            />
          </template>
        </UInput>
      </UFormField>

      <UButton
        type="submit"
        variant="solid"
        color="warning"
        size="lg"
        :loading="isSubmitting"
        :disabled="isSubmitting"
        class="font-semibold justify-center py-2 px-10 rounded-lg my-4 w-full"
      >
        Reset Password
      </UButton>
    </UForm>

    <div v-else class="space-y-4">
      <div class="flex justify-center mb-4">
        <UIcon name="i-lucide-check-circle" class="text-6xl" />
      </div>
      <h3 class="text-lg font-semibold text-center">
        Password Reset Successful!
      </h3>
      <p class="text-center text-gray-600">
        Your password has been successfully reset. You can now sign in with your
        new password.
      </p>
      <UButton
        variant="solid"
        color="warning"
        size="lg"
        class="w-full justify-center"
        to="/sign-in"
      >
        Go to Sign In
      </UButton>
    </div>

    <div v-if="!passwordReset && !tokenError" class="mt-4 text-center">
      <NuxtLink
        to="/sign-in"
        class="text-sm font-semibold underline text-default hover:text-gray-900"
      >
        Back to Sign In
      </NuxtLink>
    </div>
  </AuthFormContainer>
</template>

<script setup lang="ts">
import * as v from 'valibot';
import type { FormSubmitEvent } from '@nuxt/ui';
import { loginResetPassword } from '~/generated/api';

const route = useRoute();
const toast = useToast();

const token = ref<string>('');
const tokenError = ref(false);

const state = ref({
  password: '',
  confirmPassword: '',
});

const passwordReset = ref(false);
const isSubmitting = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);

// Validate token from query params
onMounted(() => {
  const tokenParam = route.query.token;

  if (!tokenParam || typeof tokenParam !== 'string') {
    tokenError.value = true;
    toast.add({
      title: 'Invalid reset link',
      description: 'Please request a new password reset link',
      color: 'error',
    });
  } else {
    token.value = tokenParam;
  }
});

const schemaDefinition = v.pipe(
  v.object({
    password: v.pipe(
      v.string(),
      v.nonEmpty('Password is required'),
      v.minLength(8, 'Password must be at least 8 characters long'),
      v.maxLength(128, 'Password must be at most 128 characters long')
    ),
    confirmPassword: v.pipe(
      v.string(),
      v.nonEmpty('Please confirm your password')
    ),
  }),
  v.forward(
    v.partialCheck(
      [['password'], ['confirmPassword']],
      (input) => input.password === input.confirmPassword,
      'Passwords do not match'
    ),
    ['confirmPassword']
  )
);

type Schema = v.InferOutput<typeof schemaDefinition>;

const schema = schemaDefinition;

async function onSubmit(event: FormSubmitEvent<Schema>) {
  if (!token.value) {
    toast.add({
      title: 'Error',
      description: 'Invalid reset token',
      color: 'error',
    });
    return;
  }

  isSubmitting.value = true;

  try {
    const res = await loginResetPassword({
      body: {
        token: token.value,
        new_password: event.data.password,
      },
    });

    if (!res.error) {
      passwordReset.value = true;
      toast.add({
        title: 'Success',
        description: 'Your password has been reset successfully',
        color: 'success',
      });
    } else {
      const errorMessage = extractErrorMessage(res.error);

      // Check if token is invalid
      if (errorMessage.toLowerCase().includes('invalid token')) {
        tokenError.value = true;
      }

      toast.add({
        title: 'Password reset failed',
        description: errorMessage,
        color: 'error',
      });
    }
  } catch (error) {
    console.error('Password reset failed:', error);
    toast.add({
      title: 'Something went wrong',
      description: 'Please try again later',
      color: 'error',
    });
  } finally {
    isSubmitting.value = false;
  }
}
</script>
