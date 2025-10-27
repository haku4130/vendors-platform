<template>
  <div>
    <Header />

    <UMain>
      <slot />
    </UMain>

    <UFooter>
      <p class="text-muted text-sm">
        © {{ new Date().getFullYear() }} Vendor Platform
      </p>
    </UFooter>
  </div>
</template>
