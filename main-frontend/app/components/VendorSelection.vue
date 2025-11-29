<template>
  <div class="w-full max-w-5xl rounded-xl p-8">
    <h2 class="text-2xl font-semibold">
      Select service providers to bid on your project
    </h2>
    <div class="max-w-fit mx-auto">
      <USeparator label="Or" class="my-4" />
      <p class="mb-6">
        Click “Send to Vendors” button to make your project open and you would
        just wait for proposals
      </p>
    </div>

    <div class="space-y-6">
      <div v-for="vendor in vendors" :key="vendor.id">
        <VendorCard
          :data="vendor"
          @select="handleVendorSelect"
          @add-shortlist="handleShortlist"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const handleVendorSelect = () => null;
const handleShortlist = () => null;
const vendors = [
  {
    id: 1,
    name: 'BrainRocket Studio',
    rating: 4.7,
    reviewsCount: 59,
    tags: [
      'Art Production',
      'Animation',
      '3D Modeling',
      'Concept Art',
      'UI/UX',
    ],
    minProjectSize: '$5000',
    rateRange: '$40 - $80',
    employees: '70 - 120',
    location: 'Limassol, Cyprus',
    reviews: [
      {
        id: 1,
        author: 'Alex P.',
        rating: 5,
        text: 'They delivered our project ahead of time and exceeded expectations.',
      },
      {
        id: 2,
        author: 'Marta K.',
        rating: 4,
        text: 'Very professional team, great communication throughout the process.',
      },
      {
        id: 3,
        author: 'John D.',
        rating: 5,
        text: 'Excellent work on our UI/UX design — creative and detail-oriented.',
      },
    ],
  },
  {
    id: 2,
    name: 'TechSolutions Ltd.',
    rating: 4.5,
    reviewsCount: 42,
    tags: ['Web Development', 'Mobile Apps', 'E-commerce'],
    minProjectSize: '$10000',
    rateRange: '$50 - $100',
    employees: '50 - 100',
    location: 'Moscow, Russia',
    reviews: [
      {
        id: 1,
        author: 'Anna S.',
        rating: 4,
        text: 'Great experience working with this team. They delivered on time and within budget.',
      },
      {
        id: 2,
        author: 'Michael T.',
        rating: 5,
        text: 'Highly skilled developers. They transformed our ideas into a functional product seamlessly.',
      },
      {
        id: 3,
        author: 'Sarah W.',
        rating: 4,
        text: 'Good communication and support throughout the project. Would recommend.',
      },
    ],
  },
  {
    id: 3,
    name: 'TechSolutions Ltd.',
    rating: 4.5,
    reviewsCount: 42,
    tags: ['Web Development', 'Mobile Apps', 'E-commerce'],
    minProjectSize: '$10000',
    rateRange: '$50 - $100',
    employees: '50 - 100',
    location: 'Moscow, Russia',
    reviews: [
      {
        id: 1,
        author: 'Anna S.',
        rating: 4,
        text: 'Great experience working with this team. They delivered on time and within budget.',
      },
      {
        id: 2,
        author: 'Michael T.',
        rating: 5,
        text: 'Highly skilled developers. They transformed our ideas into a functional product seamlessly.',
      },
      {
        id: 3,
        author: 'Sarah W.',
        rating: 4,
        text: 'Good communication and support throughout the project. Would recommend.',
      },
    ],
  },
];
</script>
