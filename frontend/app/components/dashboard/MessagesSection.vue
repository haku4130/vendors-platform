<template>
  <div class="space-y-8">
    <section
      class="bg-vendor-gradient shadow-sm p-6 rounded-2xl flex flex-col lg:flex-row items-stretch gap-6"
    >
      <div class="flex flex-col items-start gap-4">
        <h2 class="text-xl font-semibold text-white leading-snug">
          {{ $t('dashboard.messages.banner') }}
        </h2>
        <UButton size="xl" :to="$localePath('/dashboard/projects')"> {{ $t('dashboard.messages.findPartner') }} </UButton>
      </div>
    </section>
  </div>
</template>
