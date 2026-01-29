<template>
  <AuthFormContainer class="max-w-sm">
    <div v-if="!emailSent" class="text-start space-y-1">
      <h2 class="text-xl font-semibold text-gray-800">Forgot Password?</h2>
      <p class="text-sm mb-6 text-gray-600">
        Enter your email address and we'll send you a link to reset your
        password.
      </p>
    </div>

    <UForm v-if="!emailSent" :schema="schema" :state="state" @submit="onSubmit">
      <UFormField label="Email" name="email">
        <UInput
          v-model="state.email"
          leading-icon="i-lucide-at-sign"
          type="email"
          placeholder="your@email.com"
          class="w-full"
          :ui="{ base: 'placeholder:text-normal' }"
          :disabled="isSubmitting"
        />
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
        Send Reset Link
      </UButton>
    </UForm>

    <div v-else class="space-y-4">
      <div class="flex justify-center mb-4">
        <UIcon name="i-lucide-mail-check" class="text-6xl" />
      </div>
      <p class="text-center text-gray-700">
        If an account exists with the email
        <span class="font-semibold">{{ state.email }}</span
        >, you will receive a password reset link shortly.
      </p>
      <p class="text-sm text-center text-gray-600">
        Please check your inbox and spam folder.
      </p>
      <UButton
        variant="outline"
        size="lg"
        class="w-full my-4 justify-center"
        @click="handleSendAnother"
      >
        Send Another Email
      </UButton>
    </div>

    <div class="mt-4 text-center">
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
import { loginRecoverPassword } from '~/generated/api';

const state = ref({
  email: '',
});

const emailSent = ref(false);
const isSubmitting = ref(false);

const schemaDefinition = v.pipe(
  v.object({
    email: v.pipe(
      v.string(),
      v.nonEmpty('Email is required'),
      v.email('Please enter a valid email address'),
    ),
  }),
);

type Schema = v.InferOutput<typeof schemaDefinition>;

const schema = schemaDefinition;

const toast = useToast();

async function onSubmit(event: FormSubmitEvent<Schema>) {
  isSubmitting.value = true;

  try {
    const res = await loginRecoverPassword({
      path: {
        email: event.data.email,
      },
    });

    if (!res.error) {
      emailSent.value = true;
      toast.add({
        title: 'Email sent',
        description: 'Please check your inbox for the password reset link',
        color: 'success',
      });
    } else {
      // Still show success to prevent email enumeration
      emailSent.value = true;
      toast.add({
        title: 'Email sent',
        description: 'If an account exists, you will receive a reset link',
        color: 'success',
      });
    }
  } catch (error) {
    console.error('Password recovery failed:', error);
    toast.add({
      title: 'Something went wrong',
      description: 'Please try again later',
      color: 'error',
    });
  } finally {
    isSubmitting.value = false;
  }
}

function handleSendAnother() {
  emailSent.value = false;
  state.value.email = '';
}
</script>
