<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 gap-8 max-w-2xl">
    <UCard class="shadow-sm">
      <ImageUpload
        class="-p-6"
        :current-avatar="auth.user.value?.logo_url ?? undefined"
      />
    </UCard>

    <UCard class="bg-vendor-gradient shadow-sm h-fit">
      <template #header>
        <p class="font-semibold">General Information</p>
      </template>
      <UForm :state="form" class="space-y-4">
        <UFormField label="Full Name" name="full_name">
          <UInput v-model="form.full_name" class="w-full" />
        </UFormField>

        <UFormField label="Email" name="email">
          <UInput :model-value="form.email" disabled class="w-full" />
        </UFormField>

        <UFormField label="Company Name" name="company_name">
          <UInput :model-value="form.company_name" disabled class="w-full" />
        </UFormField>

        <UFormField label="Location" name="location">
          <LocationSelector
            v-model="form.location"
            :icon="null"
            class="w-full"
          />
        </UFormField>

        <UButton
          :loading="saving"
          color="primary"
          class="mt-3"
          @click="saveProfile"
        >
          Save Changes
        </UButton>
      </UForm>
    </UCard>
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '~/composables/useAuth';
import { usersUpdateUserMe } from '~/generated/api';

const auth = useAuth();

const form = reactive({
  full_name: auth.user.value?.full_name,
  email: auth.user.value?.email,
  company_name: auth.user.value?.company_name,
  location: auth.user.value?.location,
});

const saving = ref(false);
const toast = useToast();

async function saveProfile() {
  saving.value = true;

  const res = await usersUpdateUserMe({
    body: {
      full_name: form.full_name,
      location: form.location,
    },
  });

  saving.value = false;

  if (res.error) {
    toast.add({
      title: 'Error',
      description: extractErrorMessage(res.error, 'Could not update profile'),
      color: 'error',
    });
    return;
  }

  auth.user.value = res.data;
  toast.add({
    title: 'Success',
    description: 'Profile updated successfully!',
    color: 'success',
  });
}
</script>
