<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded-lg shadow-lg max-w-md">
      <h1 class="text-2xl font-bold text-green-600 mb-6 text-center">Green Portfolio Tracker</h1>
      <div class="mb-6">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">Add Investment</h2>
        <form @submit.prevent="addInvestment" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-600">Name</label>
            <input v-model="investment.name" required class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-600">Category</label>
            <input v-model="investment.category" value="Renewable" required class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-600">CO2 Reduction per Unit</label>
            <input type="number" step="0.1" v-model.number="investment.co2_reduction_per_unit" required class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-600">Expected Return (%)</label>
            <input type="number" step="0.1" v-model.number="investment.expected_return" required class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-600">Amount</label>
            <input type="number" step="0.1" v-model.number="investment.amount" required class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500">
          </div>
          <button type="submit" class="w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700 transition">Add Investment</button>
        </form>
        <p v-if="error" class="text-red-500 text-sm mt-2">{{ error }}</p>
      </div>
      <div>
        <h2 class="text-lg font-semibold text-gray-700 mb-2">Transaction Summary</h2>
        <p class="text-gray-600">Total CO2 Impact: <span class="font-medium">{{ summary.total_impact }}</span> kg</p>
        <p class="text-gray-600">Total Performance: <span class="font-medium">{{ summary.total_performance }}</span> %</p>
        <button @click="fetchSummary" class="mt-4 bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition">Refresh Summary</button>
        <button @click="resetSummary" class="mt-4 ml-2 bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 transition">Reset Summary</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      investment: {
        name: '',
        category: 'Renewable',
        co2_reduction_per_unit: 0,
        expected_return: 0,
        amount: 0
      },
      summary: {
        total_impact: 0,
        total_performance: 0
      },
      error: ''
    };
  },
  methods: {
    async addInvestment() {
      try {
        console.log('Adding investment:', this.investment);
        // Étape 1 : Créer l'investissement
        const investmentResponse = await fetch('http://127.0.0.1:8000/api/investments/', {
          method: 'POST',
          headers: {
            'Authorization': 'Basic dGVzdHVzZXI6dGVzdHBhc3MxMjM=',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: this.investment.name,
            category: this.investment.category,
            co2_reduction_per_unit: this.investment.co2_reduction_per_unit,
            expected_return: this.investment.expected_return
          })
        });
        if (!investmentResponse.ok) {
          const errorData = await investmentResponse.json();
          throw new Error(JSON.stringify(errorData));
        }
        const investmentData = await investmentResponse.json();
        console.log('Investment created:', investmentData);

        // Étape 2 : Créer la transaction associée
        const transactionResponse = await fetch('http://127.0.0.1:8000/api/transactions/', {
          method: 'POST',
          headers: {
            'Authorization': 'Basic dGVzdHVzZXI6dGVzdHBhc3MxMjM=',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            investment: investmentData.id,
            amount: this.investment.amount.toFixed(2)
          })
        });
        if (!transactionResponse.ok) {
          const errorData = await transactionResponse.json();
          throw new Error(JSON.stringify(errorData));
        }
        const transactionData = await transactionResponse.json();
        console.log('Transaction created:', transactionData);

        this.error = 'Investment and transaction added successfully!';
        this.investment = { name: '', category: 'Renewable', co2_reduction_per_unit: 0, expected_return: 0, amount: 0 };
        await this.fetchSummary();
      } catch (error) {
        console.error('Error adding investment:', error);
        this.error = error.message;
      }
    },
    async fetchSummary() {
      try {
        console.log('Fetching summary...');
        const response = await fetch(`http://127.0.0.1:8000/api/transactions/summary/?t=${Date.now()}`, {
          headers: {
            'Authorization': 'Basic dGVzdHVzZXI6dGVzdHBhc3MxMjM='
          }
        });
        if (!response.ok) {
          const errorData = await response.text();
          throw new Error(`Failed to fetch summary: ${errorData}`);
        }
        const data = await response.json();
        console.log('Summary received:', data);
        this.summary = data;
        this.error = '';
      } catch (error) {
        console.error('Error fetching summary:', error);
        this.error = error.message;
      }
    },
    resetSummary() {
      console.log('Resetting summary...');
      this.summary = { total_impact: 0, total_performance: 0 };
      this.error = 'Summary reset successfully!';
    }
  },
  mounted() {
    this.fetchSummary();
  }
}
</script>