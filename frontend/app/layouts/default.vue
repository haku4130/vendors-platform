<template>
  <div>
    <Header />

    <UMain class="place-content-center">
      <slot />
    </UMain>

    <UFooter>
      <p class="text-muted text-sm">
        © {{ new Date().getFullYear() }} {{ $t('brandName') }}
      </p>
    </UFooter>
  </div>
</template>
