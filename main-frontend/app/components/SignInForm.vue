<template>
  <AuthFormContainer class="max-w-sm">
    <div class="text-start space-y-1">
      <h2 class="text-xl font-semibold text-gray-800">Sign In</h2>
      <h2 class="text-sm mb-6 text-gray-600">
        Welcome back to Vendor Platform
      </h2>
    </div>

    <UForm :state="state" class="space-y-4" @submit="onSubmit">
      <UFormField label="Email" name="email">
        <UInput v-model="state.email" class="w-full" />
      </UFormField>

      <UFormField label="Password" name="password">
        <UInput
          v-model="state.password"
          class="w-full"
          :type="show ? 'text' : 'password'"
          :ui="{ trailing: 'pe-1' }"
        >
          <template #trailing>
            <UButton
              color="neutral"
              variant="link"
              size="sm"
              :icon="show ? 'i-lucide-eye-off' : 'i-lucide-eye'"
              :aria-label="show ? 'Hide password' : 'Show password'"
              :aria-pressed="show"
              aria-controls="password"
              @click="show = !show"
            />
          </template>
        </UInput>
        <template #hint>
          <NuxtLink
            to="/password-reset"
            class="font-semibold underline text-default hover:text-gray-900"
          >
            Forgot password?
          </NuxtLink>
        </template>
      </UFormField>

      <UButton
        variant="solid"
        color="warning"
        size="lg"
        label="Continue"
        class="font-semibold justify-center py-2 px-10 rounded-lg my-4"
      />
    </UForm>

    <p class="text-sm text-gray-800">
      Don't have an account?
      <NuxtLink
        to="/register"
        class="font-semibold underline hover:text-gray-900"
      >
        Register
      </NuxtLink>
    </p>
  </AuthFormContainer>
</template>

<script setup lang="ts">
import type { FormSubmitEvent } from '@nuxt/ui';

const state = ref({
  email: '',
  password: '',
});

const toast = useToast();
async function onSubmit(event: FormSubmitEvent<typeof state.value>) {
  toast.add({
    title: 'Success',
    description: 'The form has been submitted.',
    color: 'success',
  });
  console.log(event.data);
}

const show = ref(false);
</script>
