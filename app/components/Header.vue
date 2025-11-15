<template>
  <!-- <header class="hidden w-full border-b-1 sticky top-0">
    <div
      class="bg-gray-600 text-white flex items-center justify-between px-8 py-2"
    >
      <NuxtLink to="/" class="flex items-center">
        <img src="/favicon.ico" alt="Logo" class="h-8" />
      </NuxtLink>

      <div class="flex items-center gap-6">
        <div class="flex items-center bg-white rounded-full">
          <UInput
            placeholder="Search"
            icon="i-heroicons-magnifying-glass"
            variant="none"
            trailing
            size="sm"
          />
        </div>

        <nav class="flex items-center gap-6 text-sm font-medium">
          <NuxtLink to="/reviews" class="hover:text-gray-300"
            >Leave a Review</NuxtLink
          >
          <NuxtLink to="/login" class="hover:text-gray-300">Sign In</NuxtLink>
          <UButton
            variant="ghost"
            color="neutral"
            size="sm"
            label="Join"
            to="/sign-in"
            class="border-1 border-gray-200 rounded-full hover:bg-white text-white hover:text-gray-800 dark:active:bg-gray-300 px-3"
          />
        </nav>
      </div>
    </div>


    <div class="flex items-center justify-end bg-white px-8 py-3">
      <nav
        class="flex items-center gap-8 pr-6 text-sm font-semibold text-gray-800"
      >
        <NuxtLink to="/development" class="hover:text-gray-600"
          >Development</NuxtLink
        >
        <NuxtLink to="/it-services" class="hover:text-gray-600"
          >IT Services</NuxtLink
        >
        <NuxtLink to="/design" class="hover:text-gray-600">Design</NuxtLink>
        <NuxtLink to="/pricing" class="hover:text-gray-600">Pricing</NuxtLink>
      </nav>

      <NuxtLink
        to="/projects/new"
        class="text-red-600 font-semibold border-l pl-6 hover:text-red-700 border-black"
      >
        Post a Project
      </NuxtLink>
    </div>
  </header> -->

  <UHeader title="Vendor Platform" class="bg-gray-100">
    <template #right>
      <div class="flex items-center gap-6">
        <!-- Search -->
        <!-- <div class="flex items-center bg-white rounded-lg border">
          <UInput
            placeholder="Search"
            icon="i-heroicons-magnifying-glass"
            variant="none"
            trailing
            size="sm"
          />
        </div> -->

        <!-- Right links -->
        <nav class="flex items-center gap-6 text-sm font-medium">
          <UButton to="/reviews" variant="link"> Leave a Review </UButton>
          <UButton to="/dashboard" variant="link"> Dashboard </UButton>
          <UButton size="sm" label="Sign In" to="/sign-in" />
        </nav>
      </div>
    </template>
  </UHeader>
</template>
